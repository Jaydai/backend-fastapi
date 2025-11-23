-- Migration: Add Team System
-- Description: Creates tables for hierarchical team management and user-team permissions
-- Date: 2025-11-23

-- Drop existing tables if they exist (for clean migration)
DROP TABLE IF EXISTS public.user_team_permissions CASCADE;
DROP TABLE IF EXISTS public.teams CASCADE;

-- Teams table with hierarchical support
CREATE TABLE IF NOT EXISTS public.teams (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    organization_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    parent_team_id UUID REFERENCES public.teams(id) ON DELETE CASCADE,
    color TEXT DEFAULT '#3B82F6', -- Default blue color for UI
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT teams_name_org_unique UNIQUE(organization_id, name),
    CONSTRAINT teams_no_self_reference CHECK (id != parent_team_id)
);

-- User team permissions (many-to-many relationship)
CREATE TABLE IF NOT EXISTS public.user_team_permissions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    team_id UUID NOT NULL REFERENCES public.teams(id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'member', -- 'member', 'lead', 'admin'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT user_team_unique UNIQUE(user_id, team_id),
    CONSTRAINT valid_role CHECK (role IN ('member', 'lead', 'admin'))
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_teams_organization_id ON public.teams(organization_id);
CREATE INDEX IF NOT EXISTS idx_teams_parent_team_id ON public.teams(parent_team_id);
CREATE INDEX IF NOT EXISTS idx_user_team_permissions_user_id ON public.user_team_permissions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_team_permissions_team_id ON public.user_team_permissions(team_id);

-- Indexes for audit queries (optimize team-filtered queries)
CREATE INDEX IF NOT EXISTS idx_chats_user_id ON public.chats(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON public.messages(user_id);
CREATE INDEX IF NOT EXISTS idx_enriched_chats_user_id ON public.enriched_chats(user_id);
CREATE INDEX IF NOT EXISTS idx_enriched_chats_theme ON public.enriched_chats(theme);
CREATE INDEX IF NOT EXISTS idx_enriched_chats_intent ON public.enriched_chats(intent);
CREATE INDEX IF NOT EXISTS idx_enriched_chats_created_at ON public.enriched_chats(created_at);
CREATE INDEX IF NOT EXISTS idx_enriched_messages_user_id ON public.enriched_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_enriched_messages_risk_level ON public.enriched_messages(overall_risk_level);
CREATE INDEX IF NOT EXISTS idx_enriched_messages_created_at ON public.enriched_messages(created_at);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_teams_updated_at
    BEFORE UPDATE ON public.teams
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_team_permissions_updated_at
    BEFORE UPDATE ON public.user_team_permissions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to prevent circular team hierarchies
CREATE OR REPLACE FUNCTION check_team_hierarchy()
RETURNS TRIGGER AS $$
DECLARE
    current_parent_id BIGINT;
    depth INTEGER := 0;
    max_depth INTEGER := 10; -- Prevent infinite loops
BEGIN
    -- Only check if parent_team_id is being set
    IF NEW.parent_team_id IS NULL THEN
        RETURN NEW;
    END IF;

    current_parent_id := NEW.parent_team_id;

    -- Traverse up the hierarchy to check for cycles
    WHILE current_parent_id IS NOT NULL AND depth < max_depth LOOP
        -- Check if we've reached the current team (cycle detected)
        IF current_parent_id = NEW.id THEN
            RAISE EXCEPTION 'Circular team hierarchy detected';
        END IF;

        -- Move up the hierarchy
        SELECT parent_team_id INTO current_parent_id
        FROM public.teams
        WHERE id = current_parent_id;

        depth := depth + 1;
    END LOOP;

    IF depth >= max_depth THEN
        RAISE EXCEPTION 'Team hierarchy too deep (max 10 levels)';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to prevent circular hierarchies
CREATE TRIGGER prevent_circular_team_hierarchy
    BEFORE INSERT OR UPDATE ON public.teams
    FOR EACH ROW
    EXECUTE FUNCTION check_team_hierarchy();

-- Comments for documentation
COMMENT ON TABLE public.teams IS 'Organizational teams with hierarchical support';
COMMENT ON TABLE public.user_team_permissions IS 'Many-to-many relationship between users and teams with role-based permissions';
COMMENT ON COLUMN public.teams.parent_team_id IS 'Reference to parent team for hierarchical structure (NULL for root teams)';
COMMENT ON COLUMN public.teams.color IS 'Hex color code for UI representation';
COMMENT ON COLUMN public.user_team_permissions.role IS 'User role within the team: member, lead, or admin';
