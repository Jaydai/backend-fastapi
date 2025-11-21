# Database Migrations

This folder contains SQL migration scripts for the enrichment feature.

## Migration Files

### `create_enrichment_tables.sql`
Creates the enriched_chats and enriched_messages tables with all necessary indexes, constraints, and RLS policies.

**Tables Created:**
- `enriched_chats` - Stores chat classification and quality assessment data
- `enriched_messages` - Stores message risk assessment data

**Features:**
- ✅ Row Level Security (RLS) policies for data isolation
- ✅ Indexes for optimal query performance
- ✅ Foreign key constraints to auth.users
- ✅ Automatic updated_at timestamp triggers
- ✅ JSON/JSONB columns for flexible data storage
- ✅ CHECK constraints for data validation

### `rollback_enrichment_tables.sql`
Rolls back the migration by dropping all tables, indexes, and policies.

⚠️ **WARNING:** This will delete all data! Make sure to backup before running.

## How to Run Migrations

### Option 1: Supabase Dashboard (Recommended)

1. Go to your Supabase project dashboard
2. Navigate to **SQL Editor**
3. Click **New Query**
4. Copy and paste the contents of `create_enrichment_tables.sql`
5. Click **Run** or press `Ctrl+Enter`
6. Verify the success message: "Migration completed successfully!"

### Option 2: Supabase CLI

```bash
# Make sure you're in the project directory
cd /Users/quentinbragard/Jaydai/backend-fastapi

# Run the migration
supabase db execute --file migrations/create_enrichment_tables.sql

# Or if you have psql installed
psql -U postgres -h localhost -p 54322 -d postgres -f migrations/create_enrichment_tables.sql
```

### Option 3: psql Command Line

```bash
psql "postgresql://postgres:[YOUR-PASSWORD]@[YOUR-HOST]:5432/postgres" \
  -f migrations/create_enrichment_tables.sql
```

## Verifying the Migration

After running the migration, verify the tables were created:

```sql
-- Check if tables exist
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('enriched_chats', 'enriched_messages');

-- Check RLS is enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE tablename IN ('enriched_chats', 'enriched_messages');

-- View table structure
\d enriched_chats
\d enriched_messages
```

## Rolling Back

If you need to rollback the migration:

```bash
# Option 1: Supabase Dashboard
# Copy contents of rollback_enrichment_tables.sql and run in SQL Editor

# Option 2: CLI
supabase db execute --file migrations/rollback_enrichment_tables.sql

# Option 3: psql
psql "postgresql://..." -f migrations/rollback_enrichment_tables.sql
```

## Table Schemas

### enriched_chats

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| created_at | TIMESTAMPTZ | Creation timestamp |
| updated_at | TIMESTAMPTZ | Last update timestamp |
| user_id | UUID | Reference to auth.users |
| chat_id | BIGINT | Optional internal chat ID |
| chat_provider_id | TEXT | Provider's chat ID (required) |
| message_provider_id | TEXT | Provider's message ID |
| is_work_related | BOOLEAN | Classification: work vs personal |
| theme | TEXT | Chat theme/category |
| intent | TEXT | User's intent |
| quality_score | INTEGER | Overall quality (0-100) |
| clarity_score | INTEGER | Clarity score (0-5) |
| context_score | INTEGER | Context score (0-5) |
| specificity_score | INTEGER | Specificity score (0-5) |
| actionability_score | INTEGER | Actionability score (0-5) |
| feedback_summary | TEXT | AI feedback summary |
| feedback_strengths | TEXT[] | List of strengths |
| feedback_improvements | TEXT[] | List of improvements |
| improved_prompt_example | TEXT | Example of improved prompt |
| user_override_quality | BOOLEAN | User manually set quality |
| user_quality_score | INTEGER | User's quality rating (0-100) |
| raw_response | JSONB | Full AI response |
| processing_time_ms | INTEGER | Processing time in ms |
| model_used | TEXT | AI model identifier |

**Unique Constraint:** (user_id, chat_provider_id)

### enriched_messages

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| created_at | TIMESTAMPTZ | Creation timestamp |
| updated_at | TIMESTAMPTZ | Last update timestamp |
| user_id | UUID | Reference to auth.users |
| message_id | BIGINT | Optional internal message ID |
| message_provider_id | TEXT | Provider's message ID (required) |
| overall_risk_level | TEXT | none/low/medium/high/critical |
| overall_risk_score | NUMERIC(5,2) | Overall risk (0-100) |
| risk_categories | JSONB | Detailed risk by category |
| risk_summary | TEXT[] | List of risk descriptions |
| detected_issues | JSONB | Array of detected issues |
| user_whitelist | BOOLEAN | User whitelisted this message |
| processing_time_ms | INTEGER | Processing time in ms |
| model_used | TEXT | AI model identifier |

**Unique Constraint:** (user_id, message_provider_id)

### risk_categories JSON Structure

```json
{
  "pii": {
    "level": "high",
    "score": 85.5,
    "detected": true,
    "details": "Email address detected"
  },
  "security": {
    "level": "medium",
    "score": 45.0,
    "detected": true,
    "details": "API key pattern found"
  },
  "confidential": { ... },
  "misinformation": { ... },
  "data_leakage": { ... },
  "compliance": { ... }
}
```

### detected_issues JSON Structure

```json
[
  {
    "category": "pii",
    "severity": "high",
    "description": "Personal email address detected",
    "details": {
      "pattern": "email",
      "count": 1
    }
  }
]
```

## Row Level Security (RLS)

Both tables have RLS enabled with policies that ensure:

- ✅ Users can only SELECT their own data (`user_id = auth.uid()`)
- ✅ Users can only INSERT data with their own user_id
- ✅ Users can only UPDATE their own data
- ✅ Users can only DELETE their own data

This provides complete data isolation between users.

## Performance Considerations

The migration includes indexes on:

- **enriched_chats:** user_id, chat_provider_id, created_at, quality_score, is_work_related, theme, intent
- **enriched_messages:** user_id, message_provider_id, created_at, overall_risk_level, overall_risk_score, user_whitelist
- **JSONB columns:** GIN indexes on risk_categories and detected_issues for fast JSON queries

These indexes optimize common queries like:
- Finding chats/messages by user
- Filtering by risk level or quality score
- Sorting by date or score
- Searching JSON fields

## Troubleshooting

### Error: "relation already exists"

The tables already exist. Either:
1. Use the rollback script first, then re-run the migration
2. Modify the script to use `CREATE TABLE IF NOT EXISTS` (already included)

### Error: "permission denied"

Make sure you're running the script with sufficient permissions:
- In Supabase Dashboard, you're automatically authenticated
- With CLI/psql, use the `postgres` user or service_role credentials

### Error: "column does not exist"

The migration script is designed to be idempotent. If you get column errors, the table might already exist with a different schema. Use the rollback script first.

## Next Steps

After running the migration:

1. ✅ Verify tables exist and RLS is enabled
2. ✅ Test the enrichment endpoints in your FastAPI backend
3. ✅ Monitor query performance with the included indexes
4. ✅ Consider adding additional indexes based on your query patterns

## Support

For issues or questions, refer to:
- [Supabase RLS Documentation](https://supabase.com/docs/guides/auth/row-level-security)
- [PostgreSQL JSONB Documentation](https://www.postgresql.org/docs/current/datatype-json.html)
