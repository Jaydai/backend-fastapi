# Version Slug Migration

## Overview

This migration adds a `slug` column to the `prompt_templates_versions` table to enable URL-friendly version identification for organization templates.

## What This Migration Does

1. **Adds `slug` column** to `prompt_templates_versions` table
2. **Creates helper functions** for slug generation:
   - `generate_version_slug(version_name, version_number)` - Converts version names to URL-friendly slugs
   - `ensure_unique_version_slug(template_id, base_slug)` - Ensures slug uniqueness within a template
3. **Backfills existing versions** with generated slugs (e.g., "Version 2.0" → "v1-version-2-0")
4. **Adds unique constraint** on `(template_id, slug)` to prevent duplicates
5. **Creates auto-generation trigger** for new versions

## Files Created

### Migration Files
- `migrations/add_version_slug_column.sql` - Main SQL migration script
- `migrations/README_version_slug.md` - This documentation file

### Utility Files
- `utils/slug.py` - Python utility functions for slug generation (mirrors SQL functions)

### Scripts
- `scripts/apply_version_slug_migration.py` - Helper to display migration SQL
- `scripts/test_version_slug_migration.sh` - Bash script with manual migration instructions
- `scripts/verify_version_slug_migration.py` - Verification script to check migration success

## How to Apply the Migration

### Option 1: Supabase SQL Editor (Recommended)

1. Go to your Supabase project's SQL Editor: https://app.supabase.com/project/YOUR_PROJECT_REF/sql
2. Open the migration file: `migrations/add_version_slug_column.sql`
3. Copy the entire SQL content
4. Paste into the SQL Editor
5. Click "Run" to execute

### Option 2: psql Command Line

```bash
# Get your database password from Supabase dashboard settings
psql -h db.YOUR_PROJECT_REF.supabase.co \
     -U postgres \
     -d postgres \
     -f migrations/add_version_slug_column.sql
```

### Option 3: Using the Helper Script

```bash
# From the fastapi-backend directory
python3 scripts/apply_version_slug_migration.py
# This will display the SQL to copy/paste into Supabase SQL Editor
```

## How to Verify the Migration

After applying the migration, verify it was successful:

```bash
# From the fastapi-backend directory
python3 scripts/verify_version_slug_migration.py
```

This script checks:
- ✅ Slug column exists and is populated
- ✅ All slugs are unique within each template
- ✅ Slug format matches expected pattern (lowercase, hyphens, no special chars)
- ✅ Sample slugs are displayed for manual inspection

## Slug Generation Examples

The migration generates slugs based on version names:

| Version Name        | Generated Slug       | Notes                           |
|---------------------|----------------------|---------------------------------|
| "Version 2.0"       | "v1-version-2-0"     | Numbered v1, v2, v3...          |
| "Beta Release"      | "v2-beta-release"    | Spaces → hyphens                |
| "1.5 Draft"         | "v3-1-5-draft"       | Special chars → hyphens         |
| "Production"        | "v4-production"      | Simple lowercase conversion     |

## Database Schema Changes

```sql
-- New column
ALTER TABLE prompt_templates_versions
ADD COLUMN slug TEXT NOT NULL;

-- New constraint
ALTER TABLE prompt_templates_versions
ADD CONSTRAINT prompt_templates_versions_template_id_slug_key
UNIQUE (template_id, slug);

-- New index
CREATE INDEX idx_prompt_templates_versions_slug
ON prompt_templates_versions(slug);
```

## Functions Created

### `generate_version_slug(version_name TEXT, version_number INTEGER)`
Converts a version name into a URL-friendly slug.

**Example:**
```sql
SELECT generate_version_slug('Version 2.0', 1);
-- Returns: 'v1-version-2-0'
```

### `ensure_unique_version_slug(template_id UUID, base_slug TEXT)`
Ensures a slug is unique within a template by appending numbers if needed.

**Example:**
```sql
SELECT ensure_unique_version_slug('abc-123', 'v1-draft');
-- Returns: 'v1-draft' (if unique) or 'v1-draft-2', 'v1-draft-3', etc.
```

### `auto_generate_version_slug()` (Trigger Function)
Automatically generates slugs for new versions when inserted.

## Rollback

If you need to rollback this migration:

```sql
-- Remove trigger
DROP TRIGGER IF EXISTS trigger_auto_generate_version_slug ON prompt_templates_versions;

-- Remove functions
DROP FUNCTION IF EXISTS auto_generate_version_slug();
DROP FUNCTION IF EXISTS ensure_unique_version_slug(UUID, TEXT);
DROP FUNCTION IF EXISTS generate_version_slug(TEXT, INTEGER);

-- Remove constraint
ALTER TABLE prompt_templates_versions
DROP CONSTRAINT IF EXISTS prompt_templates_versions_template_id_slug_key;

-- Remove index
DROP INDEX IF EXISTS idx_prompt_templates_versions_slug;

-- Remove column
ALTER TABLE prompt_templates_versions
DROP COLUMN IF EXISTS slug;
```

## Next Steps

After successfully applying and verifying this migration:

1. ✅ **Phase 1 Complete**: Database schema updated
2. → **Phase 2**: Create DTOs (TemplateMetadataDTO, VersionSummary)
3. → **Phase 3**: Create repository methods for fetching by slug
4. → **Phase 4**: Create service methods
5. → **Phase 5**: Create organization-specific endpoints
6. → **Phase 6**: Implement frontend server actions
7. → **Phase 7**: Implement frontend routes
8. → **Phase 8**: Create client component
9. → **Phase 9**: Update ModernTemplateDetailView
10. → **Phase 10**: Implement caching strategy

## Troubleshooting

### "Column already exists" error
If you see this error, the migration may have been partially applied. Check if the column exists:
```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'prompt_templates_versions'
AND column_name = 'slug';
```

### "Duplicate slug" errors
Run the uniqueness check:
```sql
SELECT template_id, slug, COUNT(*)
FROM prompt_templates_versions
GROUP BY template_id, slug
HAVING COUNT(*) > 1;
```

### Trigger not firing
Check if trigger exists:
```sql
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE trigger_name = 'trigger_auto_generate_version_slug';
```

## Support

For issues or questions about this migration:
1. Check the verification script output
2. Review Supabase logs in the dashboard
3. Check this README for troubleshooting tips
