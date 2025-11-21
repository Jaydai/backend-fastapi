-- =====================================================
-- Add Organization Type Column
-- Adds type column to organizations table to distinguish
-- between company and standard organizations
-- =====================================================

-- Add type column to organizations table
ALTER TABLE organizations
ADD COLUMN IF NOT EXISTS type TEXT NOT NULL DEFAULT 'standard'
CHECK (type IN ('company', 'standard'));

-- Add index for faster filtering by type
CREATE INDEX IF NOT EXISTS idx_organizations_type ON organizations(type);

-- Add comment for documentation
COMMENT ON COLUMN organizations.type IS 'Organization type: company (legacy company workspaces) or standard (regular organizations)';

-- =====================================================
-- Verify column was added
-- =====================================================

DO $$
BEGIN
    IF EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'organizations'
        AND column_name = 'type'
    ) THEN
        RAISE NOTICE 'Migration completed successfully! Column organizations.type added.';
    ELSE
        RAISE EXCEPTION 'Migration failed - type column not created';
    END IF;
END $$;
