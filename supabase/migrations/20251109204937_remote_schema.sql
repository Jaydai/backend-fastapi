


SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


CREATE EXTENSION IF NOT EXISTS "pg_net" WITH SCHEMA "extensions";






COMMENT ON SCHEMA "public" IS 'standard public schema';



CREATE EXTENSION IF NOT EXISTS "pg_graphql" WITH SCHEMA "graphql";






CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgjwt" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";






CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";






CREATE TYPE "public"."permission_type" AS ENUM (
    'admin:settings',
    'comment:create',
    'comment:read',
    'comment:update',
    'comment:delete',
    'template:create',
    'template:read',
    'template:update',
    'template:delete',
    'block:create',
    'block:read',
    'block:update',
    'block:delete',
    'user:create',
    'user:read',
    'user:update',
    'user:delete',
    'organization:create',
    'organization:read',
    'organization:update',
    'organization:delete'
);


ALTER TYPE "public"."permission_type" OWNER TO "postgres";


CREATE TYPE "public"."role_type" AS ENUM (
    'admin',
    'writer',
    'viewer',
    'guest'
);


ALTER TYPE "public"."role_type" OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."cleanup_test_data"("p_org_ids" "uuid"[]) RETURNS "void"
    LANGUAGE "sql" SECURITY DEFINER
    SET "search_path" TO 'public'
    AS $$
    -- Supprimer les rôles liés aux organisations de test
    DELETE FROM user_organization_roles
    WHERE organization_id = ANY(p_org_ids)
       OR organization_id IS NULL; -- Aussi cleanup les rôles globaux de test
    
    -- Supprimer les organisations de test
    DELETE FROM organizations
    WHERE id = ANY(p_org_ids);
$$;


ALTER FUNCTION "public"."cleanup_test_data"("p_org_ids" "uuid"[]) OWNER TO "postgres";


COMMENT ON FUNCTION "public"."cleanup_test_data"("p_org_ids" "uuid"[]) IS 'Nettoyer les données de test (bypass RLS)';



CREATE OR REPLACE FUNCTION "public"."create_initial_template_version"() RETURNS "trigger"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    version_id uuid;
    template_title_en text;
    template_title_fr text;  
    author_uuid uuid;
BEGIN
    -- Get author (prefer user_id, fallback to authenticated user)
    author_uuid := COALESCE(NEW.user_id, auth.uid());
    
    -- Skip if no author identified
    IF author_uuid IS NULL THEN
        RETURN NEW;
    END IF;
    
    -- Extract titles from JSONB title field
    template_title_en := COALESCE(NEW.title->>'en', 'Untitled Template');
    template_title_fr := COALESCE(NEW.title->>'fr', template_title_en);
    
    -- Only create version if we have meaningful title content
    IF template_title_en IS NOT NULL AND template_title_en != '' THEN
        -- Insert initial version with placeholder content
        INSERT INTO public.prompt_templates_versions (
            template_id,
            version_number,
            content,
            author_id,
            is_current,
            status,
            change_notes,
            usage_count
        ) VALUES (
            NEW.id,
            '1.0', 
            jsonb_build_object('en', 'Template content will be added via version creation', 'fr', 'Le contenu du modèle sera ajouté via la création de version'),
            author_uuid,
            true,
            'draft',
            jsonb_build_object('en', 'Initial version', 'fr', 'Version initiale'),
            0
        ) RETURNING id INTO version_id;
        
        -- Update the template to reference this version (if current_version_id field exists)
        BEGIN
            UPDATE public.prompt_templates 
            SET current_version_id = version_id 
            WHERE id = NEW.id;
        EXCEPTION WHEN undefined_column THEN
            -- Ignore if current_version_id field doesn't exist yet
            NULL;
        END;
    END IF;
    
    RETURN NEW;
END;
$$;


ALTER FUNCTION "public"."create_initial_template_version"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."create_test_organization"("p_org_id" "uuid", "p_org_name" "text") RETURNS "uuid"
    LANGUAGE "sql" SECURITY DEFINER
    SET "search_path" TO 'public'
    AS $$
    INSERT INTO organizations (id, name)
    VALUES (p_org_id, p_org_name)
    ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name
    RETURNING id;
$$;


ALTER FUNCTION "public"."create_test_organization"("p_org_id" "uuid", "p_org_name" "text") OWNER TO "postgres";


COMMENT ON FUNCTION "public"."create_test_organization"("p_org_id" "uuid", "p_org_name" "text") IS 'Créer une organisation pour les tests (bypass RLS)';



CREATE OR REPLACE FUNCTION "public"."create_test_user_role"("p_user_id" "uuid", "p_role" "public"."role_type", "p_organization_id" "uuid" DEFAULT NULL::"uuid") RETURNS "uuid"
    LANGUAGE "plpgsql" SECURITY DEFINER
    SET "search_path" TO 'public'
    AS $$
DECLARE
    v_role_id UUID;
BEGIN
    -- Temporairement désactiver la vérification de la FK pour ce user_id
    -- En insérant directement (la FK sera ignorée pour les tests)
    SET CONSTRAINTS user_organization_roles_user_id_fkey DEFERRED;
    
    INSERT INTO user_organization_roles (user_id, role, organization_id)
    VALUES (p_user_id, p_role, p_organization_id)
    ON CONFLICT (user_id, organization_id, role) DO NOTHING
    RETURNING id INTO v_role_id;
    
    RETURN v_role_id;
END;
$$;


ALTER FUNCTION "public"."create_test_user_role"("p_user_id" "uuid", "p_role" "public"."role_type", "p_organization_id" "uuid") OWNER TO "postgres";


COMMENT ON FUNCTION "public"."create_test_user_role"("p_user_id" "uuid", "p_role" "public"."role_type", "p_organization_id" "uuid") IS 'Assigner un rôle à un utilisateur pour les tests (bypass RLS, accepte des user_id fictifs)';



CREATE OR REPLACE FUNCTION "public"."ensure_single_current_version"() RETURNS "trigger"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    -- If this version is being set as current, unset all other current versions for this template
    IF NEW.is_current = true THEN
        UPDATE public.prompt_templates_versions 
        SET is_current = false, updated_at = now()
        WHERE template_id = NEW.template_id 
        AND id != NEW.id 
        AND is_current = true;
    END IF;
    
    RETURN NEW;
END;
$$;


ALTER FUNCTION "public"."ensure_single_current_version"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_organization_folders"("org_id" "uuid") RETURNS TABLE("id" "uuid", "title" "jsonb", "organization_id" "uuid", "workspace_type" "text")
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
  BEGIN
      RETURN QUERY
      SELECT
          pf.id,
          pf.title,
          pf.organization_id,
          pf.workspace_type
      FROM prompt_folders pf
      WHERE pf.organization_id = org_id;
  END;
  $$;


ALTER FUNCTION "public"."get_organization_folders"("org_id" "uuid") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_organization_members"("org_id" "text") RETURNS TABLE("user_id" "uuid", "email" "text", "name" "text", "profile_picture_url" "text", "role" "text", "created_at" timestamp with time zone)
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    RETURN QUERY
    SELECT
        um.user_id,
        au.email,
        um.name,
        um.profile_picture_url,
        (um.roles->'organizations'->org_id)::TEXT as role,
        um.created_at
    FROM users_metadata um
    INNER JOIN auth.users au ON um.user_id = au.id
    WHERE um.roles->'organizations' ? org_id;
END;
$$;


ALTER FUNCTION "public"."get_organization_members"("org_id" "text") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_role_permissions"("p_role" "public"."role_type") RETURNS "public"."permission_type"[]
    LANGUAGE "plpgsql" IMMUTABLE
    AS $$
BEGIN
    RETURN CASE p_role
        WHEN 'admin' THEN ARRAY[
            'admin:settings',
            'comment:create', 'comment:read', 'comment:update', 'comment:delete',
            'template:create', 'template:read', 'template:update', 'template:delete',
            'block:create', 'block:read', 'block:update', 'block:delete',
            'user:create', 'user:read', 'user:update', 'user:delete',
            'organization:read', 'organization:update'
        ]::permission_type[]
        WHEN 'writer' THEN ARRAY[
            'comment:create', 'comment:read', 'comment:update', 'comment:delete',
            'template:create', 'template:read', 'template:update', 'template:delete',
            'block:create', 'block:read', 'block:update', 'block:delete',
            'organization:read'
        ]::permission_type[]
        WHEN 'viewer' THEN ARRAY[
            'comment:create', 'comment:read', 'comment:update', 'comment:delete',
            'template:read',
            'block:read',
            'organization:read'
        ]::permission_type[]
        WHEN 'guest' THEN ARRAY[
            'comment:read',
            'template:read',
            'block:read',
            'organization:read'
        ]::permission_type[]
        ELSE ARRAY[]::permission_type[]
    END;
END;
$$;


ALTER FUNCTION "public"."get_role_permissions"("p_role" "public"."role_type") OWNER TO "postgres";


COMMENT ON FUNCTION "public"."get_role_permissions"("p_role" "public"."role_type") IS 'Retourne la liste des permissions pour un rôle donné.
Permissions par rôle:
- admin: Toutes les permissions SAUF organization:create et organization:delete
- writer: Création/modification de contenu + organization:read
- viewer: Lecture + commentaires + organization:read
- guest: Lecture seule + organization:read

Note: Les permissions organization:create et organization:delete sont réservées aux admins globaux
via les RLS policies qui vérifient organization_id IS NULL';



CREATE OR REPLACE FUNCTION "public"."get_user_roles"("p_user_id" "uuid", "p_organization_id" "uuid" DEFAULT NULL::"uuid") RETURNS TABLE("role" "public"."role_type", "organization_id" "uuid", "permissions" "public"."permission_type"[])
    LANGUAGE "plpgsql" STABLE SECURITY DEFINER
    SET "search_path" TO 'public'
    AS $$
BEGIN
    RETURN QUERY
    SELECT
        uor.role,
        uor.organization_id,
        get_role_permissions(uor.role) as permissions
    FROM user_organization_roles uor
    WHERE uor.user_id = p_user_id
      AND (p_organization_id IS NULL
           OR uor.organization_id = p_organization_id
           OR uor.organization_id IS NULL)
    ORDER BY (uor.organization_id IS NOT NULL) DESC;
END;
$$;


ALTER FUNCTION "public"."get_user_roles"("p_user_id" "uuid", "p_organization_id" "uuid") OWNER TO "postgres";


COMMENT ON FUNCTION "public"."get_user_roles"("p_user_id" "uuid", "p_organization_id" "uuid") IS 'Retourne tous les rôles et permissions d''un utilisateur.
SECURITY DEFINER: Bypasse RLS pour éviter la récursion infinie.';



CREATE OR REPLACE FUNCTION "public"."get_user_subscription"("user_uuid" "uuid") RETURNS TABLE("is_active" boolean, "plan_id" "text", "current_period_end" timestamp with time zone, "cancel_at_period_end" boolean, "stripe_customer_id" "text", "stripe_subscription_id" "text")
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CASE 
            WHEN um.subscription_status IN ('active', 'trialing') THEN true 
            ELSE false 
        END as is_active,
        um.subscription_plan as plan_id,
        um.subscription_current_period_end as current_period_end,
        COALESCE(um.subscription_cancel_at_period_end, false) as cancel_at_period_end,
        um.stripe_customer_id as stripe_customer_id,
        um.stripe_subscription_id as stripe_subscription_id
    FROM users_metadata um
    WHERE um.user_id = user_uuid;
END;
$$;


ALTER FUNCTION "public"."get_user_subscription"("user_uuid" "uuid") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."get_user_subscription_status"("check_user_id" "uuid" DEFAULT NULL::"uuid") RETURNS TABLE("user_id" "uuid", "is_active" boolean, "plan_id" "text", "current_period_end" timestamp with time zone, "cancel_at_period_end" boolean, "has_stripe_customer" boolean)
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    target_user_id UUID;
BEGIN
    -- If no user_id provided, use the authenticated user
    IF check_user_id IS NULL THEN
        target_user_id := auth.uid();
    ELSE
        target_user_id := check_user_id;
    END IF;
    
    -- Security check: users can only access their own data
    IF (current_setting('role') != 'service_role' AND auth.uid() != target_user_id) THEN
        RAISE EXCEPTION 'Access denied: can only view your own subscription status';
    END IF;
    
    RETURN QUERY
    SELECT 
        um.user_id,
        CASE 
            WHEN um.subscription_status IN ('active', 'trialing') THEN true 
            ELSE false 
        END as is_active,
        um.subscription_plan as plan_id,
        um.subscription_current_period_end as current_period_end,
        COALESCE(um.subscription_cancel_at_period_end, false) as cancel_at_period_end,
        CASE 
            WHEN um.stripe_customer_id IS NOT NULL THEN true 
            ELSE false 
        END as has_stripe_customer
    FROM users_metadata um
    WHERE um.user_id = target_user_id;
END;
$$;


ALTER FUNCTION "public"."get_user_subscription_status"("check_user_id" "uuid") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."has_active_subscription"("user_uuid" "uuid") RETURNS boolean
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM users_metadata 
        WHERE user_id = user_uuid 
        AND subscription_status IN ('active', 'trialing')
    );
END;
$$;


ALTER FUNCTION "public"."has_active_subscription"("user_uuid" "uuid") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."log_subscription_changes"() RETURNS "trigger"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    -- Only log if subscription-related fields changed
    IF (OLD.subscription_status IS DISTINCT FROM NEW.subscription_status OR
        OLD.subscription_plan IS DISTINCT FROM NEW.subscription_plan) THEN
        
        INSERT INTO subscription_audit_log (
            user_id,
            old_status,
            new_status,
            old_plan,
            new_plan,
            changed_by,
            metadata
        ) VALUES (
            NEW.user_id,
            OLD.subscription_status,
            NEW.subscription_status,
            OLD.subscription_plan,
            NEW.subscription_plan,
            CASE 
                WHEN current_setting('role') = 'service_role' THEN 'webhook'
                ELSE 'manual'
            END,
            jsonb_build_object(
                'stripe_customer_id', NEW.stripe_customer_id,
                'stripe_subscription_id', NEW.stripe_subscription_id
            )
        );
    END IF;
    
    RETURN NEW;
END;
$$;


ALTER FUNCTION "public"."log_subscription_changes"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."prevent_stripe_column_updates"() RETURNS "trigger"
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    -- Check if any Stripe-related columns are being updated by non-service roles
    IF (current_setting('role') != 'service_role') THEN
        -- Prevent updates to critical Stripe columns
        IF (OLD.stripe_customer_id IS DISTINCT FROM NEW.stripe_customer_id OR
            OLD.subscription_status IS DISTINCT FROM NEW.subscription_status OR
            OLD.subscription_plan IS DISTINCT FROM NEW.subscription_plan OR
            OLD.stripe_subscription_id IS DISTINCT FROM NEW.stripe_subscription_id OR
            OLD.subscription_current_period_end IS DISTINCT FROM NEW.subscription_current_period_end OR
            OLD.subscription_cancel_at_period_end IS DISTINCT FROM NEW.subscription_cancel_at_period_end) THEN
            
            RAISE EXCEPTION 'Stripe subscription data can only be updated by the service'
                USING HINT = 'Use the Stripe customer portal or API to modify subscription data';
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$;


ALTER FUNCTION "public"."prevent_stripe_column_updates"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."update_current_version_id"() RETURNS "trigger"
    LANGUAGE "plpgsql"
    AS $$
BEGIN
    IF NEW.is_current = TRUE THEN
        -- Update the template's current_version_id to point to this version
        UPDATE prompt_templates 
        SET current_version_id = NEW.id
        WHERE id = NEW.template_id;
    END IF;
    RETURN NEW;
END;
$$;


ALTER FUNCTION "public"."update_current_version_id"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."update_favorites_updated_at"() RETURNS "trigger"
    LANGUAGE "plpgsql"
    AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;


ALTER FUNCTION "public"."update_favorites_updated_at"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."update_updated_at_column"() RETURNS "trigger"
    LANGUAGE "plpgsql"
    AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;


ALTER FUNCTION "public"."update_updated_at_column"() OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."user_can_delete_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") RETURNS boolean
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    -- Personal items (type = 'user'): only owner can delete
    IF item_type = 'user' AND item_user_id = auth.uid() THEN
        RETURN true;
    END IF;

    -- Company items (type = 'company'): admin+ can delete
    IF item_type = 'company' AND item_company_id IS NOT NULL THEN
        RETURN user_has_company_role(auth.uid(), item_company_id, 'admin');
    END IF;

    -- Organization items (type = 'organization'): admin+ can delete
    IF item_type = 'organization' AND item_organization_id IS NOT NULL THEN
        RETURN user_has_org_role(auth.uid(), item_organization_id, 'admin');
    END IF;

    RETURN false;
END;
$$;


ALTER FUNCTION "public"."user_can_delete_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."user_can_read_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") RETURNS boolean
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    -- Personal items (type = 'user')
    IF item_type = 'user' AND item_user_id = auth.uid() THEN
        RETURN true;
    END IF;

    -- Company items (type = 'company')
    IF item_type = 'company' AND item_company_id IS NOT NULL THEN
        RETURN user_has_company_role(auth.uid(), item_company_id, 'viewer');
    END IF;

    -- Organization items (type = 'organization')
    IF item_type = 'organization' AND item_organization_id IS NOT NULL THEN
        RETURN user_has_org_role(auth.uid(), item_organization_id, 'viewer');
    END IF;

    RETURN false;
END;
$$;


ALTER FUNCTION "public"."user_can_read_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."user_can_write_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") RETURNS boolean
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    -- Personal items (type = 'user')
    IF item_type = 'user' AND item_user_id = auth.uid() THEN
        RETURN true;
    END IF;

    -- Company items (type = 'company')
    IF item_type = 'company' AND item_company_id IS NOT NULL THEN
        RETURN user_has_company_role(auth.uid(), item_company_id, 'member');
    END IF;

    -- Organization items (type = 'organization')
    IF item_type = 'organization' AND item_organization_id IS NOT NULL THEN
        RETURN user_has_org_role(auth.uid(), item_organization_id, 'member');
    END IF;

    RETURN false;
END;
$$;


ALTER FUNCTION "public"."user_can_write_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."user_has_active_subscription"("check_user_id" "uuid" DEFAULT NULL::"uuid") RETURNS boolean
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    target_user_id UUID;
BEGIN
    -- If no user_id provided, use the authenticated user
    IF check_user_id IS NULL THEN
        target_user_id := auth.uid();
    ELSE
        target_user_id := check_user_id;
    END IF;
    
    -- Security check: users can only check their own status (unless service role)
    IF (current_setting('role') != 'service_role' AND auth.uid() != target_user_id) THEN
        RAISE EXCEPTION 'Access denied: can only check your own subscription status';
    END IF;
    
    RETURN EXISTS (
        SELECT 1 FROM users_metadata 
        WHERE user_id = target_user_id 
        AND subscription_status IN ('active', 'trialing')
    );
END;
$$;


ALTER FUNCTION "public"."user_has_active_subscription"("check_user_id" "uuid") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."user_has_company_role"("user_uuid" "uuid", "target_company_id" "uuid", "required_role" "text") RETURNS boolean
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    -- Check if user has the required role or higher for the company
    RETURN EXISTS (
        SELECT 1 FROM users_metadata
        WHERE user_id = user_uuid
        AND company_id = target_company_id
        AND CASE required_role
            WHEN 'viewer' THEN roles->>'company' IN ('viewer', 'member', 'admin', 'owner')
            WHEN 'member' THEN roles->>'company' IN ('member', 'admin', 'owner')
            WHEN 'admin' THEN roles->>'company' IN ('admin', 'owner')
            WHEN 'owner' THEN roles->>'company' = 'owner'
            ELSE FALSE
        END
    );
END;
$$;


ALTER FUNCTION "public"."user_has_company_role"("user_uuid" "uuid", "target_company_id" "uuid", "required_role" "text") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."user_has_org_role"("user_uuid" "uuid", "target_org_id" "uuid", "required_role" "text") RETURNS boolean
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
BEGIN
    -- Check if user has the required role or higher for the organization
    RETURN EXISTS (
        SELECT 1 FROM users_metadata
        WHERE user_id = user_uuid
        AND target_org_id = ANY(organization_ids)
        AND CASE required_role
            WHEN 'viewer' THEN roles->'organizations'->>(target_org_id::text) IN ('viewer', 'member', 'admin', 'owner')
            WHEN 'member' THEN roles->'organizations'->>(target_org_id::text) IN ('member', 'admin', 'owner')
            WHEN 'admin' THEN roles->'organizations'->>(target_org_id::text) IN ('admin', 'owner')
            WHEN 'owner' THEN roles->'organizations'->>(target_org_id::text) = 'owner'
            ELSE FALSE
        END
    );
END;
$$;


ALTER FUNCTION "public"."user_has_org_role"("user_uuid" "uuid", "target_org_id" "uuid", "required_role" "text") OWNER TO "postgres";


CREATE OR REPLACE FUNCTION "public"."user_has_permission"("p_user_id" "uuid", "p_permission" "public"."permission_type", "p_organization_id" "uuid" DEFAULT NULL::"uuid") RETURNS boolean
    LANGUAGE "plpgsql" STABLE
    AS $$
DECLARE
    v_role role_type;
    v_permissions permission_type[];
    v_is_global_admin BOOLEAN;
BEGIN
    -- CAS 1: Ressource d'organisation (p_organization_id fourni)
    IF p_organization_id IS NOT NULL THEN
        -- Chercher un rôle dans cette organisation spécifique
        SELECT role INTO v_role
        FROM user_organization_roles
        WHERE user_id = p_user_id
          AND organization_id = p_organization_id
        LIMIT 1;

        -- Si rôle trouvé dans l'organisation, vérifier la permission
        IF v_role IS NOT NULL THEN
            v_permissions := get_role_permissions(v_role);
            IF p_permission = ANY(v_permissions) THEN
                RETURN TRUE;  -- ✅ Permission dans l'organisation
            END IF;
        END IF;

        -- Fallback: Vérifier si admin global (accès universel)
        SELECT EXISTS (
            SELECT 1
            FROM user_organization_roles
            WHERE user_id = p_user_id
              AND organization_id IS NULL
              AND role = 'admin'
        ) INTO v_is_global_admin;

        IF v_is_global_admin THEN
            RETURN TRUE;  -- ✅ Admin global = accès universel
        END IF;

        -- ❌ Pas de rôle dans l'org et pas admin global
        RETURN FALSE;
    END IF;

    -- CAS 2: Ressource globale (p_organization_id IS NULL)
    -- ✨ Pour être globale, la ressource doit aussi avoir user_id à NULL
    -- Cette vérification se fait au niveau des RLS policies
    -- Ici on considère que si organization_id est NULL, l'accès est universel
    RETURN TRUE;
END;
$$;


ALTER FUNCTION "public"."user_has_permission"("p_user_id" "uuid", "p_permission" "public"."permission_type", "p_organization_id" "uuid") OWNER TO "postgres";


COMMENT ON FUNCTION "public"."user_has_permission"("p_user_id" "uuid", "p_permission" "public"."permission_type", "p_organization_id" "uuid") IS 'Vérifie si un utilisateur a une permission spécifique (optimisé).
Logique:
- Ressource d''organisation: vérifie rôle dans org → fallback admin global (accès universel)
- Ressource globale: TOUJOURS accessible (pas besoin de rôle)
  Note: Une ressource est globale si organization_id IS NULL ET user_id IS NULL (vérifié dans les RLS policies)
- Performance: Vérifie le cas normal d''abord, admin global en fallback
- Les rôles globaux (writer, viewer, guest) N''ONT PAS accès aux ressources d''organisations';



CREATE OR REPLACE FUNCTION "public"."user_subscription_expires_at"("check_user_id" "uuid" DEFAULT NULL::"uuid") RETURNS timestamp with time zone
    LANGUAGE "plpgsql" SECURITY DEFINER
    AS $$
DECLARE
    expiry_date TIMESTAMP WITH TIME ZONE;
    target_user_id UUID;
BEGIN
    -- If no user_id provided, use the authenticated user
    IF check_user_id IS NULL THEN
        target_user_id := auth.uid();
    ELSE
        target_user_id := check_user_id;
    END IF;
    
    -- Security check: users can only check their own status (unless service role)
    IF (current_setting('role') != 'service_role' AND auth.uid() != target_user_id) THEN
        RAISE EXCEPTION 'Access denied: can only check your own subscription expiry';
    END IF;
    
    SELECT subscription_current_period_end INTO expiry_date
    FROM users_metadata 
    WHERE user_id = target_user_id 
    AND subscription_status IN ('active', 'trialing');
    
    RETURN expiry_date;
END;
$$;


ALTER FUNCTION "public"."user_subscription_expires_at"("check_user_id" "uuid") OWNER TO "postgres";

SET default_tablespace = '';

SET default_table_access_method = "heap";


CREATE TABLE IF NOT EXISTS "public"."blog_posts" (
    "id" bigint NOT NULL,
    "title" "text" NOT NULL,
    "slug" "text" NOT NULL,
    "summary" "text" NOT NULL,
    "featured_image" "text",
    "author" "text" NOT NULL,
    "published_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "category" "text" NOT NULL,
    "tags" "text"[] DEFAULT '{}'::"text"[],
    "status" "text" DEFAULT 'draft'::"text" NOT NULL,
    "reading_time" integer DEFAULT 5 NOT NULL,
    "locale" "text" DEFAULT 'en'::"text" NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "call_to_action_metadata" "jsonb",
    "content_metadata" "jsonb"[],
    "page_metadata" "jsonb"
);


ALTER TABLE "public"."blog_posts" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."blog_posts_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE "public"."blog_posts_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."blog_posts_id_seq" OWNED BY "public"."blog_posts"."id";



CREATE TABLE IF NOT EXISTS "public"."chats" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "user_id" "uuid",
    "chat_provider_id" "text",
    "provider_name" "text",
    "title" "text"
);


ALTER TABLE "public"."chats" OWNER TO "postgres";


ALTER TABLE "public"."chats" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."chats_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."companies" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "name" "text",
    "image_url" "text"
);


ALTER TABLE "public"."companies" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."favorites" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "item_type" character varying(20) NOT NULL,
    "item_id" "uuid" NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"(),
    "favorite_type" "text",
    CONSTRAINT "favorites_item_type_check" CHECK ((("item_type")::"text" = ANY (ARRAY[('template'::character varying)::"text", ('folder'::character varying)::"text"])))
);


ALTER TABLE "public"."favorites" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."landing_page_blog_posts" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "title" "jsonb" NOT NULL,
    "slug" "text" NOT NULL,
    "excerpt" "jsonb",
    "content" "jsonb" NOT NULL,
    "author_id" "uuid",
    "published" boolean DEFAULT false,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"(),
    "image_url" "text"
);


ALTER TABLE "public"."landing_page_blog_posts" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."landing_page_contact_form" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "name" "text",
    "email" "text",
    "subject" "text",
    "message" "text",
    "company" "text"
);


ALTER TABLE "public"."landing_page_contact_form" OWNER TO "postgres";


ALTER TABLE "public"."landing_page_contact_form" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."landing_page_contact_form_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."messages" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "user_id" "uuid",
    "chat_provider_id" "text",
    "message_provider_id" "text",
    "role" "text",
    "model" "text",
    "parent_message_provider_id" "text",
    "tools" "text"[],
    "content" "text"
);


ALTER TABLE "public"."messages" OWNER TO "postgres";


ALTER TABLE "public"."messages" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."messages_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."notifications" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "user_id" "uuid",
    "read_at" timestamp with time zone,
    "type" "text",
    "title" "text",
    "body" "text",
    "metadata" "jsonb"
);


ALTER TABLE "public"."notifications" OWNER TO "postgres";


ALTER TABLE "public"."notifications" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."notifications_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."organizations" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "name" "text",
    "banner_url" "text",
    "image_url" "text",
    "website_url" "text",
    "description" "jsonb"
);


ALTER TABLE "public"."organizations" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."prompt_blocks" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "company_id" "uuid",
    "organization_id" "uuid",
    "user_id" "uuid",
    "type" "text",
    "content" "jsonb",
    "title" "jsonb",
    "description" "jsonb",
    "published" boolean DEFAULT false NOT NULL,
    "status" "text",
    "team_ids" "uuid"[],
    "workspace_type" "text" DEFAULT ''::"text" NOT NULL,
    "usage_count" bigint DEFAULT '0'::bigint,
    "updated_at" timestamp with time zone,
    CONSTRAINT "prompt_blocks_workspace_type_check" CHECK (("workspace_type" = ANY (ARRAY['user'::"text", 'company'::"text", 'organization'::"text"])))
);


ALTER TABLE "public"."prompt_blocks" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."prompt_folders" (
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "user_id" "uuid",
    "organization_id" "uuid",
    "parent_folder_id" "uuid",
    "title" "jsonb",
    "description" "jsonb",
    "company_id" "uuid",
    "workspace_type" "text" NOT NULL,
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    CONSTRAINT "prompt_folders_workspace_type_check" CHECK (("workspace_type" = ANY (ARRAY['user'::"text", 'company'::"text", 'organization'::"text"])))
);


ALTER TABLE "public"."prompt_folders" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."prompt_templates" (
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "tags" "text"[],
    "last_used_at" timestamp with time zone,
    "path" "text",
    "workspace_type" "text" NOT NULL,
    "usage_count" bigint DEFAULT '0'::bigint,
    "user_id" "uuid",
    "company_id" "uuid",
    "description" "jsonb",
    "organization_id" "uuid",
    "title" "jsonb",
    "team_ids" "uuid"[],
    "is_free" boolean DEFAULT true,
    "updated_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "folder_id" "uuid",
    "author_id" "uuid",
    "current_version_id" bigint,
    CONSTRAINT "prompt_templates_workspace_type_check" CHECK (("workspace_type" = ANY (ARRAY['user'::"text", 'company'::"text", 'organization'::"text"])))
);


ALTER TABLE "public"."prompt_templates" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."prompt_templates_comments" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "template_id" "uuid" NOT NULL,
    "version_id" bigint,
    "user_id" "uuid" NOT NULL,
    "content" "jsonb" DEFAULT '{"en": ""}'::"jsonb" NOT NULL,
    "parent_comment_id" "uuid",
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "is_resolved" boolean DEFAULT false NOT NULL,
    "mentions" "jsonb"
);


ALTER TABLE "public"."prompt_templates_comments" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."prompt_templates_versions" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "updated_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "version_number" "text" NOT NULL,
    "content" "jsonb" DEFAULT '{"en": "", "fr": ""}'::"jsonb" NOT NULL,
    "author_id" "uuid" NOT NULL,
    "usage_count" bigint DEFAULT 0 NOT NULL,
    "parent_version_id" bigint,
    "change_notes" "jsonb" DEFAULT '{"en": "", "fr": ""}'::"jsonb",
    "status" "text" DEFAULT 'draft'::"text" NOT NULL,
    "template_id" "uuid",
    "is_current" boolean DEFAULT false,
    "optimized_for" "text"[],
    "is_published" boolean DEFAULT false
);


ALTER TABLE "public"."prompt_templates_versions" OWNER TO "postgres";


ALTER TABLE "public"."prompt_templates_versions" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."prompt_templates_versions_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE IF NOT EXISTS "public"."share_invitations" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "invited_user_id" "uuid",
    "inviter_email" "text" NOT NULL,
    "inviter_name" "text" NOT NULL,
    "invited_email" "text",
    "invitation_type" "text" NOT NULL,
    "status" "text" DEFAULT 'pending'::"text" NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"(),
    "sent_at" timestamp with time zone,
    "metadata" "jsonb" DEFAULT '{}'::"jsonb",
    "locale" "text",
    "organization_id" "uuid",
    "inviter_user_id" "uuid",
    CONSTRAINT "valid_friend_invitation" CHECK (((("invitation_type" = 'friend'::"text") AND ("invited_email" IS NOT NULL)) OR ("invitation_type" = ANY (ARRAY['team'::"text", 'referral'::"text", 'organization'::"text"]))))
);


ALTER TABLE "public"."share_invitations" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."stripe_subscriptions" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "stripe_customer_id" "text" NOT NULL,
    "stripe_subscription_id" "text" NOT NULL,
    "stripe_price_id" "text" NOT NULL,
    "stripe_product_id" "text" NOT NULL,
    "status" "text" NOT NULL,
    "current_period_start" timestamp with time zone,
    "current_period_end" timestamp with time zone,
    "cancel_at_period_end" boolean DEFAULT false,
    "cancelled_at" timestamp with time zone,
    "trial_start" timestamp with time zone,
    "trial_end" timestamp with time zone,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "updated_at" timestamp with time zone DEFAULT "now"(),
    "metadata" "jsonb" DEFAULT '{}'::"jsonb"
);


ALTER TABLE "public"."stripe_subscriptions" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."stripe_webhook_events" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "stripe_event_id" character varying(255) NOT NULL,
    "event_type" character varying(100) NOT NULL,
    "event_data" "jsonb" NOT NULL,
    "processed" boolean DEFAULT false,
    "created_at" timestamp with time zone DEFAULT "now"(),
    "processed_at" timestamp with time zone
);


ALTER TABLE "public"."stripe_webhook_events" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."subscription_audit_log" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "old_status" "text",
    "new_status" "text",
    "old_plan" "text",
    "new_plan" "text",
    "stripe_event_id" "text",
    "changed_by" "text",
    "changed_at" timestamp with time zone DEFAULT "now"(),
    "metadata" "jsonb"
);


ALTER TABLE "public"."subscription_audit_log" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."teams" (
    "id" "uuid" DEFAULT "gen_random_uuid"() NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "company_id" "uuid",
    "name" "jsonb",
    "description" "jsonb",
    "parent_team_id" "uuid",
    "team_admins" "uuid"[]
);


ALTER TABLE "public"."teams" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."user_organization_roles" (
    "id" "uuid" DEFAULT "extensions"."uuid_generate_v4"() NOT NULL,
    "user_id" "uuid" NOT NULL,
    "organization_id" "uuid",
    "role" "public"."role_type" NOT NULL
);


ALTER TABLE "public"."user_organization_roles" OWNER TO "postgres";


COMMENT ON TABLE "public"."user_organization_roles" IS 'Table de mapping entre utilisateurs, rôles et organisations. Supporte les rôles globaux (organization_id NULL) et les rôles par organisation.';



COMMENT ON COLUMN "public"."user_organization_roles"."user_id" IS 'ID de l''utilisateur (référence auth.users)';



COMMENT ON COLUMN "public"."user_organization_roles"."organization_id" IS 'ID de l''organisation (NULL pour rôle global)';



COMMENT ON COLUMN "public"."user_organization_roles"."role" IS 'Nom du rôle assigné (admin, writer, viewer, guest)';



CREATE TABLE IF NOT EXISTS "public"."users_metadata" (
    "id" bigint NOT NULL,
    "created_at" timestamp with time zone DEFAULT "now"() NOT NULL,
    "user_id" "uuid",
    "name" "text",
    "phone_number" "text",
    "pinned_official_folder_ids" bigint[],
    "pinned_organization_folder_ids" bigint[],
    "preferences_metadata" "jsonb",
    "additional_email" "text",
    "additional_organization" "text",
    "linkedin_headline" "text",
    "linkedin_id" "text",
    "linkedin_profile_url" "text",
    "email" "text",
    "google_id" "text",
    "company_id" "uuid",
    "interests" "text"[],
    "job_industry" "text",
    "job_seniority" "text",
    "job_type" "text",
    "organization_ids" "uuid"[],
    "pinned_folder_ids" "text"[],
    "pinned_template_ids" "text"[],
    "signup_source" "text",
    "pinned_block_ids" bigint[],
    "profile_picture_url" "text",
    "roles" "jsonb",
    "data_collection" boolean DEFAULT false,
    "first_block_created" boolean DEFAULT false,
    "first_template_created" boolean DEFAULT false,
    "first_template_used" boolean DEFAULT false,
    "keyboard_shortcut_used" boolean DEFAULT false,
    "onboarding_dismissed" boolean DEFAULT false,
    "stripe_customer_id" character varying(255),
    "stripe_subscription_id" character varying(255),
    "subscription_cancel_at_period_end" boolean DEFAULT false,
    "subscription_current_period_end" timestamp with time zone,
    "subscription_plan" character varying(50),
    "subscription_status" character varying(50) DEFAULT 'free'::character varying
);


ALTER TABLE "public"."users_metadata" OWNER TO "postgres";


ALTER TABLE "public"."users_metadata" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."users_metadata_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



ALTER TABLE ONLY "public"."blog_posts" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."blog_posts_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."blog_posts"
    ADD CONSTRAINT "blog_posts_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."blog_posts"
    ADD CONSTRAINT "blog_posts_slug_key" UNIQUE ("slug");



ALTER TABLE ONLY "public"."chats"
    ADD CONSTRAINT "chats_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."companies"
    ADD CONSTRAINT "companies_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."favorites"
    ADD CONSTRAINT "favorites_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."favorites"
    ADD CONSTRAINT "favorites_user_id_item_type_item_id_key" UNIQUE ("user_id", "item_type", "item_id");



ALTER TABLE ONLY "public"."landing_page_contact_form"
    ADD CONSTRAINT "landing_page_contact_form_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."messages"
    ADD CONSTRAINT "messages_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."notifications"
    ADD CONSTRAINT "notifications_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."organizations"
    ADD CONSTRAINT "organizations_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."prompt_blocks"
    ADD CONSTRAINT "prompt_blocks_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."prompt_folders"
    ADD CONSTRAINT "prompt_folders_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."prompt_templates_comments"
    ADD CONSTRAINT "prompt_template_comments_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."prompt_templates"
    ADD CONSTRAINT "prompt_templates_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."prompt_templates_versions"
    ADD CONSTRAINT "prompt_templates_versions_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."share_invitations"
    ADD CONSTRAINT "share_invitations_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."stripe_subscriptions"
    ADD CONSTRAINT "stripe_subscriptions_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."stripe_subscriptions"
    ADD CONSTRAINT "stripe_subscriptions_stripe_subscription_id_key" UNIQUE ("stripe_subscription_id");



ALTER TABLE ONLY "public"."stripe_webhook_events"
    ADD CONSTRAINT "stripe_webhook_events_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."stripe_webhook_events"
    ADD CONSTRAINT "stripe_webhook_events_stripe_event_id_key" UNIQUE ("stripe_event_id");



ALTER TABLE ONLY "public"."subscription_audit_log"
    ADD CONSTRAINT "subscription_audit_log_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."teams"
    ADD CONSTRAINT "teams_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."user_organization_roles"
    ADD CONSTRAINT "user_organization_roles_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."user_organization_roles"
    ADD CONSTRAINT "user_organization_roles_user_id_organization_id_role_key" UNIQUE ("user_id", "organization_id", "role");



ALTER TABLE ONLY "public"."users_metadata"
    ADD CONSTRAINT "users_metadata_pkey" PRIMARY KEY ("id");



CREATE INDEX "idx_blog_posts_category" ON "public"."blog_posts" USING "btree" ("category");



CREATE INDEX "idx_blog_posts_locale" ON "public"."blog_posts" USING "btree" ("locale");



CREATE INDEX "idx_blog_posts_published_at" ON "public"."blog_posts" USING "btree" ("published_at");



CREATE INDEX "idx_blog_posts_slug" ON "public"."blog_posts" USING "btree" ("slug");



CREATE INDEX "idx_blog_posts_status" ON "public"."blog_posts" USING "btree" ("status");



CREATE INDEX "idx_favorites_created_at" ON "public"."favorites" USING "btree" ("created_at" DESC);



CREATE INDEX "idx_favorites_item_type" ON "public"."favorites" USING "btree" ("item_type");



CREATE INDEX "idx_favorites_user_id" ON "public"."favorites" USING "btree" ("user_id");



CREATE INDEX "idx_favorites_user_item" ON "public"."favorites" USING "btree" ("user_id", "item_type");



CREATE INDEX "idx_prompt_folders_parent_folder_id" ON "public"."prompt_folders" USING "btree" ("parent_folder_id");



CREATE INDEX "idx_prompt_template_comments_created_at" ON "public"."prompt_templates_comments" USING "btree" ("created_at" DESC);



CREATE INDEX "idx_prompt_template_comments_parent_id" ON "public"."prompt_templates_comments" USING "btree" ("parent_comment_id");



CREATE INDEX "idx_prompt_template_comments_template_id" ON "public"."prompt_templates_comments" USING "btree" ("template_id");



CREATE INDEX "idx_prompt_template_comments_user_id" ON "public"."prompt_templates_comments" USING "btree" ("user_id");



CREATE INDEX "idx_prompt_template_comments_version_id" ON "public"."prompt_templates_comments" USING "btree" ("version_id");



CREATE INDEX "idx_prompt_templates_versions_author_id" ON "public"."prompt_templates_versions" USING "btree" ("author_id");



CREATE INDEX "idx_prompt_templates_versions_parent_version_id" ON "public"."prompt_templates_versions" USING "btree" ("parent_version_id") WHERE ("parent_version_id" IS NOT NULL);



CREATE INDEX "idx_prompt_templates_versions_template_id" ON "public"."prompt_templates_versions" USING "btree" ("template_id");



CREATE INDEX "idx_prompt_templates_versions_version_number" ON "public"."prompt_templates_versions" USING "btree" ("version_number");



CREATE INDEX "idx_share_invitations_org_status" ON "public"."share_invitations" USING "btree" ("organization_id", "status");



CREATE INDEX "idx_share_invitations_org_type_status" ON "public"."share_invitations" USING "btree" ("organization_id", "invitation_type", "status");



CREATE INDEX "idx_share_invitations_organization_id" ON "public"."share_invitations" USING "btree" ("organization_id");



CREATE INDEX "idx_share_invitations_status" ON "public"."share_invitations" USING "btree" ("status");



CREATE INDEX "idx_share_invitations_type" ON "public"."share_invitations" USING "btree" ("invitation_type");



CREATE INDEX "idx_share_invitations_user_id" ON "public"."share_invitations" USING "btree" ("invited_user_id");



CREATE INDEX "idx_stripe_webhook_events_processed" ON "public"."stripe_webhook_events" USING "btree" ("processed");



CREATE INDEX "idx_stripe_webhook_events_stripe_id" ON "public"."stripe_webhook_events" USING "btree" ("stripe_event_id");



CREATE INDEX "idx_stripe_webhook_events_type" ON "public"."stripe_webhook_events" USING "btree" ("event_type");



CREATE INDEX "idx_user_org_roles_org_id" ON "public"."user_organization_roles" USING "btree" ("organization_id");



CREATE INDEX "idx_user_org_roles_role" ON "public"."user_organization_roles" USING "btree" ("role");



CREATE INDEX "idx_user_org_roles_user_id" ON "public"."user_organization_roles" USING "btree" ("user_id");



CREATE INDEX "idx_user_org_roles_user_org" ON "public"."user_organization_roles" USING "btree" ("user_id", "organization_id");



CREATE INDEX "idx_users_metadata_linkedin_id" ON "public"."users_metadata" USING "btree" ("linkedin_id");



CREATE INDEX "idx_users_metadata_stripe_customer" ON "public"."users_metadata" USING "btree" ("stripe_customer_id");



CREATE INDEX "idx_users_metadata_stripe_subscription" ON "public"."users_metadata" USING "btree" ("stripe_subscription_id");



CREATE INDEX "idx_users_metadata_subscription_status" ON "public"."users_metadata" USING "btree" ("subscription_status");



CREATE OR REPLACE TRIGGER "ensure_single_current_version_trigger" BEFORE INSERT OR UPDATE ON "public"."prompt_templates_versions" FOR EACH ROW EXECUTE FUNCTION "public"."ensure_single_current_version"();



CREATE OR REPLACE TRIGGER "prevent_stripe_updates_trigger" BEFORE UPDATE ON "public"."users_metadata" FOR EACH ROW EXECUTE FUNCTION "public"."prevent_stripe_column_updates"();



CREATE OR REPLACE TRIGGER "subscription_audit_trigger" AFTER UPDATE ON "public"."users_metadata" FOR EACH ROW EXECUTE FUNCTION "public"."log_subscription_changes"();



CREATE OR REPLACE TRIGGER "update_favorites_updated_at_trigger" BEFORE UPDATE ON "public"."favorites" FOR EACH ROW EXECUTE FUNCTION "public"."update_favorites_updated_at"();



CREATE OR REPLACE TRIGGER "update_prompt_template_comments_updated_at" BEFORE UPDATE ON "public"."prompt_templates_comments" FOR EACH ROW EXECUTE FUNCTION "public"."update_updated_at_column"();



CREATE OR REPLACE TRIGGER "update_prompt_templates_updated_at" BEFORE UPDATE ON "public"."prompt_templates" FOR EACH ROW EXECUTE FUNCTION "public"."update_updated_at_column"();



CREATE OR REPLACE TRIGGER "update_prompt_templates_versions_updated_at" BEFORE UPDATE ON "public"."prompt_templates_versions" FOR EACH ROW EXECUTE FUNCTION "public"."update_updated_at_column"();



CREATE OR REPLACE TRIGGER "update_user_org_roles_updated_at" BEFORE UPDATE ON "public"."user_organization_roles" FOR EACH ROW EXECUTE FUNCTION "public"."update_updated_at_column"();



ALTER TABLE ONLY "public"."chats"
    ADD CONSTRAINT "chats_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."favorites"
    ADD CONSTRAINT "favorites_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."share_invitations"
    ADD CONSTRAINT "fk_share_invitations_organization" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."messages"
    ADD CONSTRAINT "messages_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."notifications"
    ADD CONSTRAINT "notifications_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."prompt_folders"
    ADD CONSTRAINT "prompt_folders_company_id_fkey" FOREIGN KEY ("company_id") REFERENCES "public"."companies"("id");



ALTER TABLE ONLY "public"."prompt_folders"
    ADD CONSTRAINT "prompt_folders_organization_id_fkey" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id");



ALTER TABLE ONLY "public"."prompt_folders"
    ADD CONSTRAINT "prompt_folders_parent_folder_id_fkey" FOREIGN KEY ("parent_folder_id") REFERENCES "public"."prompt_folders"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."prompt_folders"
    ADD CONSTRAINT "prompt_folders_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."prompt_templates_comments"
    ADD CONSTRAINT "prompt_template_comments_parent_comment_id_fkey" FOREIGN KEY ("parent_comment_id") REFERENCES "public"."prompt_templates_comments"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."prompt_templates_comments"
    ADD CONSTRAINT "prompt_template_comments_template_id_fkey" FOREIGN KEY ("template_id") REFERENCES "public"."prompt_templates"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."prompt_templates_comments"
    ADD CONSTRAINT "prompt_template_comments_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."prompt_templates_comments"
    ADD CONSTRAINT "prompt_template_comments_version_id_fkey" FOREIGN KEY ("version_id") REFERENCES "public"."prompt_templates_versions"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."prompt_templates"
    ADD CONSTRAINT "prompt_templates_author_id_fkey" FOREIGN KEY ("author_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."prompt_templates"
    ADD CONSTRAINT "prompt_templates_company_id_fkey" FOREIGN KEY ("company_id") REFERENCES "public"."companies"("id");



ALTER TABLE ONLY "public"."prompt_templates"
    ADD CONSTRAINT "prompt_templates_current_version_id_fkey" FOREIGN KEY ("current_version_id") REFERENCES "public"."prompt_templates_versions"("id");



ALTER TABLE ONLY "public"."prompt_templates"
    ADD CONSTRAINT "prompt_templates_folder_id_fkey" FOREIGN KEY ("folder_id") REFERENCES "public"."prompt_folders"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."prompt_templates"
    ADD CONSTRAINT "prompt_templates_organization_id_fkey" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id");



ALTER TABLE ONLY "public"."prompt_templates"
    ADD CONSTRAINT "prompt_templates_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."prompt_templates_versions"
    ADD CONSTRAINT "prompt_templates_versions_author_id_fkey" FOREIGN KEY ("author_id") REFERENCES "auth"."users"("id") ON DELETE RESTRICT;



ALTER TABLE ONLY "public"."prompt_templates_versions"
    ADD CONSTRAINT "prompt_templates_versions_parent_version_id_fkey" FOREIGN KEY ("parent_version_id") REFERENCES "public"."prompt_templates_versions"("id") ON DELETE SET NULL;



ALTER TABLE ONLY "public"."prompt_templates_versions"
    ADD CONSTRAINT "prompt_templates_versions_template_id_fkey" FOREIGN KEY ("template_id") REFERENCES "public"."prompt_templates"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."share_invitations"
    ADD CONSTRAINT "share_invitations_invited_user_id_fkey" FOREIGN KEY ("invited_user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."share_invitations"
    ADD CONSTRAINT "share_invitations_inviter_user_id_fkey" FOREIGN KEY ("inviter_user_id") REFERENCES "auth"."users"("id");



ALTER TABLE ONLY "public"."stripe_subscriptions"
    ADD CONSTRAINT "stripe_subscriptions_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."teams"
    ADD CONSTRAINT "teams_company_id_fkey" FOREIGN KEY ("company_id") REFERENCES "public"."companies"("id");



ALTER TABLE ONLY "public"."user_organization_roles"
    ADD CONSTRAINT "user_organization_roles_organization_id_fkey" FOREIGN KEY ("organization_id") REFERENCES "public"."organizations"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."user_organization_roles"
    ADD CONSTRAINT "user_organization_roles_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id") ON DELETE CASCADE DEFERRABLE;



ALTER TABLE ONLY "public"."users_metadata"
    ADD CONSTRAINT "users_metadata_company_id_fkey" FOREIGN KEY ("company_id") REFERENCES "public"."companies"("id");



ALTER TABLE ONLY "public"."users_metadata"
    ADD CONSTRAINT "users_metadata_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "auth"."users"("id");



CREATE POLICY "Allow service role full access" ON "public"."user_organization_roles" TO "service_role" USING (true) WITH CHECK (true);



CREATE POLICY "Allow webhook insertion" ON "public"."stripe_webhook_events" FOR INSERT TO "anon" WITH CHECK (true);



CREATE POLICY "Blocks delete access" ON "public"."prompt_blocks" FOR DELETE TO "authenticated" USING ("public"."user_can_delete_item"("user_id", "company_id", "organization_id", "workspace_type"));



CREATE POLICY "Blocks insert access" ON "public"."prompt_blocks" FOR INSERT TO "authenticated" WITH CHECK ("public"."user_can_write_item"("user_id", "company_id", "organization_id", "workspace_type"));



CREATE POLICY "Blocks read access" ON "public"."prompt_blocks" FOR SELECT TO "authenticated" USING ("public"."user_can_read_item"("user_id", "company_id", "organization_id", "workspace_type"));



CREATE POLICY "Blocks update access" ON "public"."prompt_blocks" FOR UPDATE TO "authenticated" USING ("public"."user_can_write_item"("user_id", "company_id", "organization_id", "workspace_type")) WITH CHECK ("public"."user_can_write_item"("user_id", "company_id", "organization_id", "workspace_type"));



CREATE POLICY "Comments delete own" ON "public"."prompt_templates_comments" FOR DELETE TO "authenticated" USING (("user_id" = "auth"."uid"()));



CREATE POLICY "Comments insert access" ON "public"."prompt_templates_comments" FOR INSERT TO "authenticated" WITH CHECK ((("user_id" = "auth"."uid"()) AND (EXISTS ( SELECT 1
   FROM "public"."prompt_templates" "pt"
  WHERE (("pt"."id" = "prompt_templates_comments"."template_id") AND "public"."user_can_read_item"("pt"."user_id", "pt"."company_id", "pt"."organization_id", "pt"."workspace_type"))))));



CREATE POLICY "Comments read access" ON "public"."prompt_templates_comments" FOR SELECT TO "authenticated" USING ((EXISTS ( SELECT 1
   FROM "public"."prompt_templates" "pt"
  WHERE (("pt"."id" = "prompt_templates_comments"."template_id") AND "public"."user_can_read_item"("pt"."user_id", "pt"."company_id", "pt"."organization_id", "pt"."workspace_type")))));



CREATE POLICY "Comments update own" ON "public"."prompt_templates_comments" FOR UPDATE TO "authenticated" USING (("user_id" = "auth"."uid"())) WITH CHECK (("user_id" = "auth"."uid"()));



CREATE POLICY "Enable insert access for all users" ON "public"."landing_page_contact_form" FOR INSERT WITH CHECK (true);



CREATE POLICY "Enable insert access for all users" ON "public"."share_invitations" FOR INSERT WITH CHECK (true);



CREATE POLICY "Enable insert for authenticated users only" ON "public"."stripe_subscriptions" FOR INSERT TO "authenticated" WITH CHECK (true);



CREATE POLICY "Enable insert for service role only" ON "public"."notifications" FOR INSERT TO "service_role" WITH CHECK (true);



CREATE POLICY "Enable insert for users based on user_id" ON "public"."chats" FOR INSERT TO "authenticated" WITH CHECK ((( SELECT "auth"."uid"() AS "uid") = "user_id"));



CREATE POLICY "Enable insert for users based on user_id" ON "public"."messages" FOR INSERT TO "authenticated" WITH CHECK ((( SELECT "auth"."uid"() AS "uid") = "user_id"));



CREATE POLICY "Enable insert for users based on user_id" ON "public"."users_metadata" FOR INSERT TO "authenticated" WITH CHECK ((( SELECT "auth"."uid"() AS "uid") = "user_id"));



CREATE POLICY "Enable read access for all users" ON "public"."blog_posts" FOR SELECT USING (true);



CREATE POLICY "Enable read access for all users" ON "public"."share_invitations" FOR SELECT USING (true);



CREATE POLICY "Enable read access for all users" ON "public"."stripe_subscriptions" FOR SELECT USING (true);



CREATE POLICY "Enable read for users based on user_id" ON "public"."chats" FOR SELECT TO "authenticated" USING ((( SELECT "auth"."uid"() AS "uid") = "user_id"));



CREATE POLICY "Enable read for users based on user_id" ON "public"."messages" FOR SELECT TO "authenticated" USING ((( SELECT "auth"."uid"() AS "uid") = "user_id"));



CREATE POLICY "Enable read for users based on user_id" ON "public"."notifications" FOR SELECT TO "authenticated" USING ((( SELECT "auth"."uid"() AS "uid") = "user_id"));



CREATE POLICY "Enable read for users based on user_id" ON "public"."users_metadata" FOR SELECT TO "authenticated" USING ((( SELECT "auth"."uid"() AS "uid") = "user_id"));



CREATE POLICY "Enable update for users based on user_id" ON "public"."users_metadata" FOR UPDATE TO "authenticated" USING ((( SELECT "auth"."uid"() AS "uid") = "user_id")) WITH CHECK ((( SELECT "auth"."uid"() AS "uid") = "user_id"));



CREATE POLICY "Enable update for version authors" ON "public"."prompt_templates_versions" FOR UPDATE TO "authenticated" USING (("author_id" = "auth"."uid"())) WITH CHECK (("author_id" = "auth"."uid"()));



CREATE POLICY "Folders delete access" ON "public"."prompt_folders" FOR DELETE TO "authenticated" USING ("public"."user_can_delete_item"("user_id", "company_id", "organization_id", "workspace_type"));



CREATE POLICY "Folders insert access" ON "public"."prompt_folders" FOR INSERT TO "authenticated" WITH CHECK ("public"."user_can_write_item"("user_id", "company_id", "organization_id", "workspace_type"));



CREATE POLICY "Folders read access" ON "public"."prompt_folders" FOR SELECT TO "authenticated" USING ("public"."user_can_read_item"("user_id", "company_id", "organization_id", "workspace_type"));



CREATE POLICY "Folders update access" ON "public"."prompt_folders" FOR UPDATE TO "authenticated" USING ("public"."user_can_write_item"("user_id", "company_id", "organization_id", "workspace_type")) WITH CHECK ("public"."user_can_write_item"("user_id", "company_id", "organization_id", "workspace_type"));



CREATE POLICY "Organizations create with permissions" ON "public"."organizations" FOR INSERT TO "authenticated" WITH CHECK ("public"."user_has_permission"("auth"."uid"(), 'organization:create'::"public"."permission_type", NULL::"uuid"));



COMMENT ON POLICY "Organizations create with permissions" ON "public"."organizations" IS 'Création d''organizations:
- Seuls les admins globaux peuvent créer des organizations
- Vérifié via user_has_permission avec organization_id = NULL';



CREATE POLICY "Organizations delete with permissions" ON "public"."organizations" FOR DELETE TO "authenticated" USING ("public"."user_has_permission"("auth"."uid"(), 'organization:delete'::"public"."permission_type", NULL::"uuid"));



COMMENT ON POLICY "Organizations delete with permissions" ON "public"."organizations" IS 'Suppression d''organizations:
- Seuls les admins globaux peuvent supprimer des organizations
- Vérifié via user_has_permission avec organization_id = NULL';



CREATE POLICY "Organizations read with permissions" ON "public"."organizations" FOR SELECT TO "authenticated" USING ("public"."user_has_permission"("auth"."uid"(), 'organization:read'::"public"."permission_type", "id"));



COMMENT ON POLICY "Organizations read with permissions" ON "public"."organizations" IS 'Lecture des organizations:
- L''utilisateur doit avoir la permission organization:read dans cette organization
- Vérifié via user_has_permission avec l''organization_id';



CREATE POLICY "Organizations service role full access" ON "public"."organizations" TO "service_role" USING (true) WITH CHECK (true);



CREATE POLICY "Organizations update with permissions" ON "public"."organizations" FOR UPDATE TO "authenticated" USING ("public"."user_has_permission"("auth"."uid"(), 'organization:update'::"public"."permission_type", "id")) WITH CHECK ("public"."user_has_permission"("auth"."uid"(), 'organization:update'::"public"."permission_type", "id"));



COMMENT ON POLICY "Organizations update with permissions" ON "public"."organizations" IS 'Modification d''organizations:
- L''utilisateur doit avoir la permission organization:update dans cette organization
- Typiquement réservé aux admins de l''organization';



CREATE POLICY "Service role can manage audit log" ON "public"."subscription_audit_log" TO "service_role" USING (true) WITH CHECK (true);



CREATE POLICY "Service role full access" ON "public"."prompt_templates_versions" TO "service_role" USING (true) WITH CHECK (true);



CREATE POLICY "Service role full access comments" ON "public"."prompt_templates_comments" TO "service_role" USING (true) WITH CHECK (true);



CREATE POLICY "Service role full access folders" ON "public"."prompt_folders" TO "service_role" USING (true) WITH CHECK (true);



CREATE POLICY "Service role full access template versions" ON "public"."prompt_templates_versions" TO "service_role" USING (true) WITH CHECK (true);



CREATE POLICY "Service role full access to webhook events" ON "public"."stripe_webhook_events" TO "service_role" USING (true) WITH CHECK (true);



CREATE POLICY "Template versions read access" ON "public"."prompt_templates_versions" FOR SELECT TO "authenticated" USING ((EXISTS ( SELECT 1
   FROM "public"."prompt_templates" "pt"
  WHERE ((("pt"."id")::"text" = ("prompt_templates_versions"."template_id")::"text") AND (("pt"."user_id" = "auth"."uid"()) OR (("pt"."company_id" IS NOT NULL) AND "public"."user_has_company_role"("auth"."uid"(), "pt"."company_id", 'viewer'::"text")) OR (("pt"."organization_id" IS NOT NULL) AND "public"."user_has_org_role"("auth"."uid"(), "pt"."organization_id", 'viewer'::"text")))))));



CREATE POLICY "Template versions write access" ON "public"."prompt_templates_versions" TO "authenticated" USING ((EXISTS ( SELECT 1
   FROM "public"."prompt_templates" "pt"
  WHERE ((("pt"."id")::"text" = ("prompt_templates_versions"."template_id")::"text") AND (("pt"."user_id" = "auth"."uid"()) OR (("pt"."company_id" IS NOT NULL) AND "public"."user_has_company_role"("auth"."uid"(), "pt"."company_id", 'member'::"text")) OR (("pt"."organization_id" IS NOT NULL) AND "public"."user_has_org_role"("auth"."uid"(), "pt"."organization_id", 'member'::"text"))))))) WITH CHECK ((EXISTS ( SELECT 1
   FROM "public"."prompt_templates" "pt"
  WHERE ((("pt"."id")::"text" = ("prompt_templates_versions"."template_id")::"text") AND (("pt"."user_id" = "auth"."uid"()) OR (("pt"."company_id" IS NOT NULL) AND "public"."user_has_company_role"("auth"."uid"(), "pt"."company_id", 'member'::"text")) OR (("pt"."organization_id" IS NOT NULL) AND "public"."user_has_org_role"("auth"."uid"(), "pt"."organization_id", 'member'::"text")))))));



CREATE POLICY "Templates create with permissions" ON "public"."prompt_templates" FOR INSERT TO "authenticated" WITH CHECK ((("user_id" IS NOT NULL) AND "public"."user_has_permission"("auth"."uid"(), 'template:create'::"public"."permission_type", "organization_id")));



COMMENT ON POLICY "Templates create with permissions" ON "public"."prompt_templates" IS 'Création de templates:
- Interdiction de créer des ressources globales (user_id obligatoire)
- Vérification des permissions pour les ressources d''organisation';



CREATE POLICY "Templates delete with permissions" ON "public"."prompt_templates" FOR DELETE TO "authenticated" USING ((("user_id" IS NOT NULL) AND "public"."user_has_permission"("auth"."uid"(), 'template:delete'::"public"."permission_type", "organization_id")));



COMMENT ON POLICY "Templates delete with permissions" ON "public"."prompt_templates" IS 'Suppression de templates:
- Ressources globales (user_id IS NULL) non supprimables
- Vérification des permissions pour les ressources d''organisation';



CREATE POLICY "Templates read with permissions" ON "public"."prompt_templates" FOR SELECT TO "authenticated" USING (((("organization_id" IS NULL) AND ("user_id" IS NULL)) OR "public"."user_has_permission"("auth"."uid"(), 'template:read'::"public"."permission_type", "organization_id")));



COMMENT ON POLICY "Templates read with permissions" ON "public"."prompt_templates" IS 'Lecture des templates: 
- Ressources globales (organization_id IS NULL AND user_id IS NULL) → accès universel
- Ressources d''organisation → vérification des permissions via user_has_permission()';



CREATE POLICY "Templates update with permissions" ON "public"."prompt_templates" FOR UPDATE TO "authenticated" USING ((("user_id" IS NOT NULL) AND "public"."user_has_permission"("auth"."uid"(), 'template:update'::"public"."permission_type", "organization_id"))) WITH CHECK ((("user_id" IS NOT NULL) AND "public"."user_has_permission"("auth"."uid"(), 'template:update'::"public"."permission_type", "organization_id")));



COMMENT ON POLICY "Templates update with permissions" ON "public"."prompt_templates" IS 'Modification de templates:
- Ressources globales (user_id IS NULL) non modifiables
- Vérification des permissions pour les ressources d''organisation';



CREATE POLICY "Users can create their own favorites" ON "public"."favorites" FOR INSERT TO "authenticated" WITH CHECK (("user_id" = "auth"."uid"()));



CREATE POLICY "Users can create their own invitations" ON "public"."share_invitations" FOR INSERT WITH CHECK (("auth"."uid"() = "invited_user_id"));



CREATE POLICY "Users can delete their own favorites" ON "public"."favorites" FOR DELETE TO "authenticated" USING (("user_id" = "auth"."uid"()));



CREATE POLICY "Users can update their own invitations" ON "public"."share_invitations" FOR UPDATE USING (("auth"."uid"() = "invited_user_id"));



CREATE POLICY "Users can view own audit log" ON "public"."subscription_audit_log" FOR SELECT TO "authenticated" USING (("auth"."uid"() = "user_id"));



CREATE POLICY "Users can view their own favorites" ON "public"."favorites" FOR SELECT TO "authenticated" USING (("user_id" = "auth"."uid"()));



CREATE POLICY "Users can view their own invitations" ON "public"."share_invitations" FOR SELECT USING (("auth"."uid"() = "invited_user_id"));



CREATE POLICY "Users can view their own roles" ON "public"."user_organization_roles" FOR SELECT TO "authenticated" USING (("user_id" = "auth"."uid"()));



ALTER TABLE "public"."blog_posts" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."chats" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."companies" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."favorites" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."landing_page_blog_posts" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."landing_page_contact_form" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."messages" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."notifications" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."organizations" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."prompt_blocks" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."prompt_folders" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."prompt_templates" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."prompt_templates_comments" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."prompt_templates_versions" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."share_invitations" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."stripe_subscriptions" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."stripe_webhook_events" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."subscription_audit_log" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."teams" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."user_organization_roles" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."users_metadata" ENABLE ROW LEVEL SECURITY;




ALTER PUBLICATION "supabase_realtime" OWNER TO "postgres";





GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";

















































































































































































GRANT ALL ON FUNCTION "public"."cleanup_test_data"("p_org_ids" "uuid"[]) TO "anon";
GRANT ALL ON FUNCTION "public"."cleanup_test_data"("p_org_ids" "uuid"[]) TO "authenticated";
GRANT ALL ON FUNCTION "public"."cleanup_test_data"("p_org_ids" "uuid"[]) TO "service_role";



GRANT ALL ON FUNCTION "public"."create_initial_template_version"() TO "anon";
GRANT ALL ON FUNCTION "public"."create_initial_template_version"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."create_initial_template_version"() TO "service_role";



GRANT ALL ON FUNCTION "public"."create_test_organization"("p_org_id" "uuid", "p_org_name" "text") TO "anon";
GRANT ALL ON FUNCTION "public"."create_test_organization"("p_org_id" "uuid", "p_org_name" "text") TO "authenticated";
GRANT ALL ON FUNCTION "public"."create_test_organization"("p_org_id" "uuid", "p_org_name" "text") TO "service_role";



GRANT ALL ON FUNCTION "public"."create_test_user_role"("p_user_id" "uuid", "p_role" "public"."role_type", "p_organization_id" "uuid") TO "anon";
GRANT ALL ON FUNCTION "public"."create_test_user_role"("p_user_id" "uuid", "p_role" "public"."role_type", "p_organization_id" "uuid") TO "authenticated";
GRANT ALL ON FUNCTION "public"."create_test_user_role"("p_user_id" "uuid", "p_role" "public"."role_type", "p_organization_id" "uuid") TO "service_role";



GRANT ALL ON FUNCTION "public"."ensure_single_current_version"() TO "anon";
GRANT ALL ON FUNCTION "public"."ensure_single_current_version"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."ensure_single_current_version"() TO "service_role";



GRANT ALL ON FUNCTION "public"."get_organization_folders"("org_id" "uuid") TO "anon";
GRANT ALL ON FUNCTION "public"."get_organization_folders"("org_id" "uuid") TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_organization_folders"("org_id" "uuid") TO "service_role";



GRANT ALL ON FUNCTION "public"."get_organization_members"("org_id" "text") TO "anon";
GRANT ALL ON FUNCTION "public"."get_organization_members"("org_id" "text") TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_organization_members"("org_id" "text") TO "service_role";



GRANT ALL ON FUNCTION "public"."get_role_permissions"("p_role" "public"."role_type") TO "anon";
GRANT ALL ON FUNCTION "public"."get_role_permissions"("p_role" "public"."role_type") TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_role_permissions"("p_role" "public"."role_type") TO "service_role";



GRANT ALL ON FUNCTION "public"."get_user_roles"("p_user_id" "uuid", "p_organization_id" "uuid") TO "anon";
GRANT ALL ON FUNCTION "public"."get_user_roles"("p_user_id" "uuid", "p_organization_id" "uuid") TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_user_roles"("p_user_id" "uuid", "p_organization_id" "uuid") TO "service_role";



GRANT ALL ON FUNCTION "public"."get_user_subscription"("user_uuid" "uuid") TO "anon";
GRANT ALL ON FUNCTION "public"."get_user_subscription"("user_uuid" "uuid") TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_user_subscription"("user_uuid" "uuid") TO "service_role";



GRANT ALL ON FUNCTION "public"."get_user_subscription_status"("check_user_id" "uuid") TO "anon";
GRANT ALL ON FUNCTION "public"."get_user_subscription_status"("check_user_id" "uuid") TO "authenticated";
GRANT ALL ON FUNCTION "public"."get_user_subscription_status"("check_user_id" "uuid") TO "service_role";



GRANT ALL ON FUNCTION "public"."has_active_subscription"("user_uuid" "uuid") TO "anon";
GRANT ALL ON FUNCTION "public"."has_active_subscription"("user_uuid" "uuid") TO "authenticated";
GRANT ALL ON FUNCTION "public"."has_active_subscription"("user_uuid" "uuid") TO "service_role";



GRANT ALL ON FUNCTION "public"."log_subscription_changes"() TO "anon";
GRANT ALL ON FUNCTION "public"."log_subscription_changes"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."log_subscription_changes"() TO "service_role";



GRANT ALL ON FUNCTION "public"."prevent_stripe_column_updates"() TO "anon";
GRANT ALL ON FUNCTION "public"."prevent_stripe_column_updates"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."prevent_stripe_column_updates"() TO "service_role";



GRANT ALL ON FUNCTION "public"."update_current_version_id"() TO "anon";
GRANT ALL ON FUNCTION "public"."update_current_version_id"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."update_current_version_id"() TO "service_role";



GRANT ALL ON FUNCTION "public"."update_favorites_updated_at"() TO "anon";
GRANT ALL ON FUNCTION "public"."update_favorites_updated_at"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."update_favorites_updated_at"() TO "service_role";



GRANT ALL ON FUNCTION "public"."update_updated_at_column"() TO "anon";
GRANT ALL ON FUNCTION "public"."update_updated_at_column"() TO "authenticated";
GRANT ALL ON FUNCTION "public"."update_updated_at_column"() TO "service_role";



GRANT ALL ON FUNCTION "public"."user_can_delete_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") TO "anon";
GRANT ALL ON FUNCTION "public"."user_can_delete_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") TO "authenticated";
GRANT ALL ON FUNCTION "public"."user_can_delete_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") TO "service_role";



GRANT ALL ON FUNCTION "public"."user_can_read_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") TO "anon";
GRANT ALL ON FUNCTION "public"."user_can_read_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") TO "authenticated";
GRANT ALL ON FUNCTION "public"."user_can_read_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") TO "service_role";



GRANT ALL ON FUNCTION "public"."user_can_write_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") TO "anon";
GRANT ALL ON FUNCTION "public"."user_can_write_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") TO "authenticated";
GRANT ALL ON FUNCTION "public"."user_can_write_item"("item_user_id" "uuid", "item_company_id" "uuid", "item_organization_id" "uuid", "item_type" "text") TO "service_role";



GRANT ALL ON FUNCTION "public"."user_has_active_subscription"("check_user_id" "uuid") TO "anon";
GRANT ALL ON FUNCTION "public"."user_has_active_subscription"("check_user_id" "uuid") TO "authenticated";
GRANT ALL ON FUNCTION "public"."user_has_active_subscription"("check_user_id" "uuid") TO "service_role";



GRANT ALL ON FUNCTION "public"."user_has_company_role"("user_uuid" "uuid", "target_company_id" "uuid", "required_role" "text") TO "anon";
GRANT ALL ON FUNCTION "public"."user_has_company_role"("user_uuid" "uuid", "target_company_id" "uuid", "required_role" "text") TO "authenticated";
GRANT ALL ON FUNCTION "public"."user_has_company_role"("user_uuid" "uuid", "target_company_id" "uuid", "required_role" "text") TO "service_role";



GRANT ALL ON FUNCTION "public"."user_has_org_role"("user_uuid" "uuid", "target_org_id" "uuid", "required_role" "text") TO "anon";
GRANT ALL ON FUNCTION "public"."user_has_org_role"("user_uuid" "uuid", "target_org_id" "uuid", "required_role" "text") TO "authenticated";
GRANT ALL ON FUNCTION "public"."user_has_org_role"("user_uuid" "uuid", "target_org_id" "uuid", "required_role" "text") TO "service_role";



GRANT ALL ON FUNCTION "public"."user_has_permission"("p_user_id" "uuid", "p_permission" "public"."permission_type", "p_organization_id" "uuid") TO "anon";
GRANT ALL ON FUNCTION "public"."user_has_permission"("p_user_id" "uuid", "p_permission" "public"."permission_type", "p_organization_id" "uuid") TO "authenticated";
GRANT ALL ON FUNCTION "public"."user_has_permission"("p_user_id" "uuid", "p_permission" "public"."permission_type", "p_organization_id" "uuid") TO "service_role";



GRANT ALL ON FUNCTION "public"."user_subscription_expires_at"("check_user_id" "uuid") TO "anon";
GRANT ALL ON FUNCTION "public"."user_subscription_expires_at"("check_user_id" "uuid") TO "authenticated";
GRANT ALL ON FUNCTION "public"."user_subscription_expires_at"("check_user_id" "uuid") TO "service_role";


















GRANT ALL ON TABLE "public"."blog_posts" TO "anon";
GRANT ALL ON TABLE "public"."blog_posts" TO "authenticated";
GRANT ALL ON TABLE "public"."blog_posts" TO "service_role";



GRANT ALL ON SEQUENCE "public"."blog_posts_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."blog_posts_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."blog_posts_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."chats" TO "anon";
GRANT ALL ON TABLE "public"."chats" TO "authenticated";
GRANT ALL ON TABLE "public"."chats" TO "service_role";



GRANT ALL ON SEQUENCE "public"."chats_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."chats_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."chats_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."companies" TO "anon";
GRANT ALL ON TABLE "public"."companies" TO "authenticated";
GRANT ALL ON TABLE "public"."companies" TO "service_role";



GRANT ALL ON TABLE "public"."favorites" TO "anon";
GRANT ALL ON TABLE "public"."favorites" TO "authenticated";
GRANT ALL ON TABLE "public"."favorites" TO "service_role";



GRANT ALL ON TABLE "public"."landing_page_blog_posts" TO "anon";
GRANT ALL ON TABLE "public"."landing_page_blog_posts" TO "authenticated";
GRANT ALL ON TABLE "public"."landing_page_blog_posts" TO "service_role";



GRANT ALL ON TABLE "public"."landing_page_contact_form" TO "anon";
GRANT ALL ON TABLE "public"."landing_page_contact_form" TO "authenticated";
GRANT ALL ON TABLE "public"."landing_page_contact_form" TO "service_role";



GRANT ALL ON SEQUENCE "public"."landing_page_contact_form_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."landing_page_contact_form_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."landing_page_contact_form_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."messages" TO "anon";
GRANT ALL ON TABLE "public"."messages" TO "authenticated";
GRANT ALL ON TABLE "public"."messages" TO "service_role";



GRANT ALL ON SEQUENCE "public"."messages_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."messages_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."messages_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."notifications" TO "anon";
GRANT ALL ON TABLE "public"."notifications" TO "authenticated";
GRANT ALL ON TABLE "public"."notifications" TO "service_role";



GRANT ALL ON SEQUENCE "public"."notifications_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."notifications_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."notifications_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."organizations" TO "anon";
GRANT ALL ON TABLE "public"."organizations" TO "authenticated";
GRANT ALL ON TABLE "public"."organizations" TO "service_role";



GRANT ALL ON TABLE "public"."prompt_blocks" TO "anon";
GRANT ALL ON TABLE "public"."prompt_blocks" TO "authenticated";
GRANT ALL ON TABLE "public"."prompt_blocks" TO "service_role";



GRANT ALL ON TABLE "public"."prompt_folders" TO "anon";
GRANT ALL ON TABLE "public"."prompt_folders" TO "authenticated";
GRANT ALL ON TABLE "public"."prompt_folders" TO "service_role";



GRANT ALL ON TABLE "public"."prompt_templates" TO "anon";
GRANT ALL ON TABLE "public"."prompt_templates" TO "authenticated";
GRANT ALL ON TABLE "public"."prompt_templates" TO "service_role";



GRANT ALL ON TABLE "public"."prompt_templates_comments" TO "anon";
GRANT ALL ON TABLE "public"."prompt_templates_comments" TO "authenticated";
GRANT ALL ON TABLE "public"."prompt_templates_comments" TO "service_role";



GRANT ALL ON TABLE "public"."prompt_templates_versions" TO "anon";
GRANT ALL ON TABLE "public"."prompt_templates_versions" TO "authenticated";
GRANT ALL ON TABLE "public"."prompt_templates_versions" TO "service_role";



GRANT ALL ON SEQUENCE "public"."prompt_templates_versions_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."prompt_templates_versions_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."prompt_templates_versions_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."share_invitations" TO "anon";
GRANT ALL ON TABLE "public"."share_invitations" TO "authenticated";
GRANT ALL ON TABLE "public"."share_invitations" TO "service_role";



GRANT ALL ON TABLE "public"."stripe_subscriptions" TO "anon";
GRANT ALL ON TABLE "public"."stripe_subscriptions" TO "authenticated";
GRANT ALL ON TABLE "public"."stripe_subscriptions" TO "service_role";



GRANT ALL ON TABLE "public"."stripe_webhook_events" TO "anon";
GRANT ALL ON TABLE "public"."stripe_webhook_events" TO "authenticated";
GRANT ALL ON TABLE "public"."stripe_webhook_events" TO "service_role";



GRANT ALL ON TABLE "public"."subscription_audit_log" TO "anon";
GRANT ALL ON TABLE "public"."subscription_audit_log" TO "authenticated";
GRANT ALL ON TABLE "public"."subscription_audit_log" TO "service_role";



GRANT ALL ON TABLE "public"."teams" TO "anon";
GRANT ALL ON TABLE "public"."teams" TO "authenticated";
GRANT ALL ON TABLE "public"."teams" TO "service_role";



GRANT ALL ON TABLE "public"."user_organization_roles" TO "anon";
GRANT ALL ON TABLE "public"."user_organization_roles" TO "authenticated";
GRANT ALL ON TABLE "public"."user_organization_roles" TO "service_role";



GRANT ALL ON TABLE "public"."users_metadata" TO "anon";
GRANT ALL ON TABLE "public"."users_metadata" TO "authenticated";
GRANT ALL ON TABLE "public"."users_metadata" TO "service_role";



GRANT ALL ON SEQUENCE "public"."users_metadata_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."users_metadata_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."users_metadata_id_seq" TO "service_role";









ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "service_role";































