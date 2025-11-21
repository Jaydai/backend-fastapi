-- =====================================================
-- Rollback Organization Type Column
-- Removes the type column from organizations table
-- =====================================================

-- WARNING: This will remove the type column and its data
-- Make sure to backup if needed!

-- Drop the index first
DROP INDEX IF EXISTS idx_organizations_type;

-- Drop the type column
ALTER TABLE organizations
DROP COLUMN IF EXISTS type;

-- =====================================================
-- Verify rollback
-- =====================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'organizations'
        AND column_name = 'type'
    ) THEN
        RAISE NOTICE 'Rollback completed successfully! Column organizations.type removed.';
    ELSE
        RAISE EXCEPTION 'Rollback failed - type column still exists';
    END IF;
END $$;
