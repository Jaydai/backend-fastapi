-- Migration: Add slug column to prompt_templates_versions table
-- Date: 2025-11-23
-- Description: Add a URL-friendly slug column for version identification and backfill existing versions

-- Step 1: Add the slug column (nullable initially for backfill)
ALTER TABLE prompt_templates_versions
ADD COLUMN IF NOT EXISTS slug TEXT;

-- Step 2: Create a function to generate slugs from version names
CREATE OR REPLACE FUNCTION generate_version_slug(version_name TEXT, version_number INTEGER DEFAULT NULL)
RETURNS TEXT AS $$
DECLARE
  slug TEXT;
BEGIN
  -- Convert to lowercase
  slug := LOWER(version_name);

  -- Replace spaces and special characters with hyphens
  slug := REGEXP_REPLACE(slug, '[^a-z0-9]+', '-', 'g');

  -- Remove leading/trailing hyphens
  slug := TRIM(BOTH '-' FROM slug);

  -- Collapse multiple consecutive hyphens
  slug := REGEXP_REPLACE(slug, '-+', '-', 'g');

  -- Prefix with version number if provided
  IF version_number IS NOT NULL THEN
    IF slug != '' THEN
      slug := 'v' || version_number || '-' || slug;
    ELSE
      slug := 'v' || version_number;
    END IF;
  END IF;

  -- Ensure the slug is not empty
  IF slug = '' THEN
    slug := 'version';
  END IF;

  RETURN slug;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Step 3: Create a function to ensure unique slugs within a template
CREATE OR REPLACE FUNCTION ensure_unique_version_slug(
  template_id UUID,
  base_slug TEXT
)
RETURNS TEXT AS $$
DECLARE
  unique_slug TEXT;
  counter INTEGER := 2;
BEGIN
  unique_slug := base_slug;

  -- Check if the slug already exists for this template
  WHILE EXISTS (
    SELECT 1 FROM prompt_templates_versions
    WHERE prompt_templates_versions.template_id = ensure_unique_version_slug.template_id
    AND slug = unique_slug
  ) LOOP
    unique_slug := base_slug || '-' || counter;
    counter := counter + 1;
  END LOOP;

  RETURN unique_slug;
END;
$$ LANGUAGE plpgsql;

-- Step 4: Backfill existing versions with generated slugs
-- For each template, generate slugs based on version name
DO $$
DECLARE
  version_record RECORD;
  base_slug TEXT;
  unique_slug TEXT;
  version_counter INTEGER;
BEGIN
  -- Process each version ordered by template and creation date
  FOR version_record IN
    SELECT
      id,
      template_id,
      name,
      ROW_NUMBER() OVER (PARTITION BY template_id ORDER BY created_at) as version_num
    FROM prompt_templates_versions
    WHERE slug IS NULL
    ORDER BY template_id, created_at
  LOOP
    -- Generate base slug from version name
    base_slug := generate_version_slug(
      version_record.name,
      version_record.version_num::INTEGER
    );

    -- Ensure uniqueness within the template
    unique_slug := ensure_unique_version_slug(
      version_record.template_id,
      base_slug
    );

    -- Update the version with the generated slug
    UPDATE prompt_templates_versions
    SET slug = unique_slug
    WHERE id = version_record.id;

    RAISE NOTICE 'Generated slug % for version % (template %)',
      unique_slug, version_record.name, version_record.template_id;
  END LOOP;
END $$;

-- Step 5: Make slug NOT NULL after backfill
ALTER TABLE prompt_templates_versions
ALTER COLUMN slug SET NOT NULL;

-- Step 6: Create a unique constraint on (template_id, slug)
-- This ensures each slug is unique within a template
ALTER TABLE prompt_templates_versions
ADD CONSTRAINT prompt_templates_versions_template_id_slug_key
UNIQUE (template_id, slug);

-- Step 7: Create an index on slug for faster lookups
CREATE INDEX IF NOT EXISTS idx_prompt_templates_versions_slug
ON prompt_templates_versions(slug);

-- Step 8: Create a trigger to auto-generate slugs for new versions
CREATE OR REPLACE FUNCTION auto_generate_version_slug()
RETURNS TRIGGER AS $$
DECLARE
  base_slug TEXT;
  version_num INTEGER;
BEGIN
  -- Only generate if slug is not provided
  IF NEW.slug IS NULL OR NEW.slug = '' THEN
    -- Get the version number for this template
    SELECT COUNT(*) + 1 INTO version_num
    FROM prompt_templates_versions
    WHERE template_id = NEW.template_id;

    -- Generate base slug
    base_slug := generate_version_slug(NEW.name, version_num);

    -- Ensure uniqueness
    NEW.slug := ensure_unique_version_slug(NEW.template_id, base_slug);
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auto_generate_version_slug
BEFORE INSERT ON prompt_templates_versions
FOR EACH ROW
EXECUTE FUNCTION auto_generate_version_slug();

-- Migration complete
-- Summary:
-- - Added slug column to prompt_templates_versions
-- - Created helper functions for slug generation
-- - Backfilled all existing versions with unique slugs
-- - Added NOT NULL constraint and unique index
-- - Created trigger for auto-generating slugs on new versions
