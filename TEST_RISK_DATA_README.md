# Test Risk Data for Audit Dashboard

## Problem

The current seed data (`current_tables_seed.sql`) contains only enriched messages with `overall_risk_level = 'none'`. This means:
- Risk tables show no data
- Risk charts show no data
- Risk categories endpoint returns empty results

All risk-related queries filter out messages where `overall_risk_level = 'none'` (see `audit_analytics_service.py` line 490), so no risk data appears in the UI.

## Solution

The `test_risk_data.sql` file adds 6 test messages with various risk levels:

1. **High Risk** - PII detected (email, phone)
2. **Critical Risk** - Security credentials (API key, password)
3. **Medium Risk** - Confidential business data
4. **Low Risk** - Minor PII (first name)
5. **High Risk** - Multiple categories (PII, security, compliance)
6. **Critical Risk** - Data leakage (database credentials, source code)

## How to Apply

### Option 1: Using psql (Recommended)
```bash
psql "postgresql://postgres:postgres@localhost:54321/postgres" -f test_risk_data.sql
```

### Option 2: Using Supabase Studio
1. Open Supabase Studio (http://localhost:54323)
2. Go to SQL Editor
3. Copy the contents of `test_risk_data.sql`
4. Run the SQL

### Option 3: Using the Supabase CLI
```bash
supabase db execute -f test_risk_data.sql
```

## What You'll See

After applying this data, the audit dashboard will show:

### Risk Categories Chart
- **pii**: 3 occurrences (1 low, 2 high)
- **security**: 3 occurrences (1 medium, 2 critical)
- **compliance**: 3 occurrences (1 medium, 2 high, 1 critical)
- **confidential**: 4 occurrences (3 medium, 1 critical)
- **data_leakage**: 4 occurrences (1 low, 1 medium, 2 critical)

### Risk Distribution by Severity
- **Critical**: 2 messages (33%)
- **High**: 2 messages (33%)
- **Medium**: 1 message (17%)
- **Low**: 1 message (17%)

### Timeline
Messages are distributed over several days in October 2025, so risk timeline charts will show trends.

## Data Details

All test messages:
- Belong to user `eff2a1fd-210c-4b44-9a6f-81af6534c3c8`
- Have unique `message_provider_id` values starting with `test-msg-`
- Include realistic `risk_categories` JSON with detected issues
- Have processing times and model information

## Reverting

To remove the test data:

```sql
DELETE FROM enriched_messages WHERE message_provider_id LIKE 'test-msg-%';
SELECT pg_catalog.setval('"public"."enriched_messages_id_seq"', 132, true);
```

## Notes

- These test messages have IDs 1001-1006 to avoid conflicts with existing seed data (which uses IDs up to ~143)
- The sequence is updated to 1006 after insertion
- All timestamps are in October 2025 to be within typical 30-day query ranges
- Risk scores and categories follow realistic patterns based on the enrichment service logic
