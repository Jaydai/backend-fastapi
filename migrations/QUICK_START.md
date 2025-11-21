# Quick Start: Enrichment Tables Migration

## 🚀 Run the Migration (3 Steps)

### Step 1: Open Supabase SQL Editor

1. Go to your Supabase dashboard: https://app.supabase.com
2. Select your project
3. Navigate to **SQL Editor** (in the left sidebar)
4. Click **New Query**

### Step 2: Run the Migration

1. Open `create_enrichment_tables.sql` in your editor
2. Copy the entire contents
3. Paste into the Supabase SQL Editor
4. Click **Run** or press `Ctrl+Enter`
5. Wait for the success message: ✅ "Migration completed successfully!"

### Step 3: Verify the Migration

1. Create a new query in Supabase SQL Editor
2. Open `verify_migration.sql` in your editor
3. Copy and paste the contents
4. Click **Run**
5. Check the output for: ✅ "MIGRATION VERIFICATION PASSED"

## ✅ What Was Created

### Tables
- **enriched_chats** - 20+ columns for chat classification and quality
- **enriched_messages** - 10+ columns for message risk assessment

### Security
- ✅ Row Level Security (RLS) enabled
- ✅ 4 policies per table (SELECT, INSERT, UPDATE, DELETE)
- ✅ User data isolation (users can only access their own data)

### Performance
- ✅ 7+ indexes on enriched_chats
- ✅ 8+ indexes on enriched_messages
- ✅ GIN indexes for fast JSON queries

### Automation
- ✅ Automatic `updated_at` timestamp triggers
- ✅ Foreign key constraints to auth.users
- ✅ Data validation with CHECK constraints

## 🧪 Test the Tables

After migration, test with a simple query:

```sql
-- Test enriched_chats table
SELECT * FROM enriched_chats LIMIT 1;

-- Test enriched_messages table
SELECT * FROM enriched_messages LIMIT 1;

-- Check your user_id (you'll need this for testing)
SELECT auth.uid() as your_user_id;
```

## 🔄 Need to Rollback?

If something goes wrong:

1. Open `rollback_enrichment_tables.sql`
2. Copy contents to SQL Editor
3. Run the query
4. Tables will be dropped (⚠️ data will be lost!)

## 📊 View Table Structure

```sql
-- View enriched_chats structure
\d enriched_chats

-- View enriched_messages structure
\d enriched_messages

-- List all indexes
\di enriched*

-- List all policies
\dp enriched*
```

## 🛠️ Troubleshooting

### "relation already exists"
- Tables already created. Either use rollback first or skip migration.

### "permission denied"
- Make sure you're using the Supabase SQL Editor (automatically authenticated)
- Or use service_role credentials with CLI

### Migration verification fails
- Review the detailed output from `verify_migration.sql`
- Check for missing indexes or policies
- Ensure RLS is enabled

## 📝 Next Steps

After successful migration:

1. ✅ Test enrichment endpoints in your FastAPI backend
2. ✅ Send test requests to `/enrichment/enrich-chat`
3. ✅ Send test requests to `/enrichment/enrich-message`
4. ✅ Verify data is being saved correctly
5. ✅ Check query performance with your data

## 🎯 Quick Test with FastAPI

```bash
# Start your backend
cd /Users/quentinbragard/Jaydai/backend-fastapi
python -m uvicorn main:app --reload

# Test enrichment endpoint (in another terminal)
curl -X POST http://localhost:8000/enrichment/enrich-chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "chat_id": 123,
    "chat_provider_id": "test-chat-1",
    "user_message": "How do I write a Python function?",
    "assistant_response": "Here is how to write a function..."
  }'
```

## 📚 Full Documentation

For detailed information, see:
- `README.md` - Complete documentation
- `create_enrichment_tables.sql` - Migration script
- `verify_migration.sql` - Verification script
- `rollback_enrichment_tables.sql` - Rollback script

## ✨ You're Done!

Your database is now ready for the enrichment feature! 🎉
