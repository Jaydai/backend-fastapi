-- =====================================================
-- Verification Script for Enrichment Tables Migration
-- Run this after the migration to verify everything is correct
-- =====================================================

\echo '========================================='
\echo 'Enrichment Tables Migration Verification'
\echo '========================================='
\echo ''

-- =====================================================
-- 1. Check if tables exist
-- =====================================================

\echo '1. Checking if tables exist...'
SELECT
    table_name,
    CASE
        WHEN table_name IN ('enriched_chats', 'enriched_messages') THEN '✓ EXISTS'
        ELSE '✗ MISSING'
    END as status
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('enriched_chats', 'enriched_messages')
ORDER BY table_name;

\echo ''

-- =====================================================
-- 2. Verify RLS is enabled
-- =====================================================

\echo '2. Verifying Row Level Security (RLS)...'
SELECT
    tablename,
    CASE
        WHEN rowsecurity THEN '✓ ENABLED'
        ELSE '✗ DISABLED'
    END as rls_status
FROM pg_tables
WHERE tablename IN ('enriched_chats', 'enriched_messages')
ORDER BY tablename;

\echo ''

-- =====================================================
-- 3. Check RLS policies
-- =====================================================

\echo '3. Checking RLS policies...'
SELECT
    tablename,
    policyname,
    cmd as operation,
    CASE
        WHEN qual IS NOT NULL THEN '✓ HAS POLICY'
        ELSE '✗ NO POLICY'
    END as status
FROM pg_policies
WHERE tablename IN ('enriched_chats', 'enriched_messages')
ORDER BY tablename, policyname;

\echo ''

-- =====================================================
-- 4. Verify indexes
-- =====================================================

\echo '4. Verifying indexes...'
SELECT
    tablename,
    indexname,
    CASE
        WHEN indexdef LIKE '%UNIQUE%' THEN 'UNIQUE'
        WHEN indexdef LIKE '%GIN%' THEN 'GIN'
        ELSE 'BTREE'
    END as index_type
FROM pg_indexes
WHERE tablename IN ('enriched_chats', 'enriched_messages')
ORDER BY tablename, indexname;

\echo ''

-- =====================================================
-- 5. Check column counts
-- =====================================================

\echo '5. Verifying column counts...'
SELECT
    table_name,
    COUNT(*) as column_count,
    CASE
        WHEN table_name = 'enriched_chats' AND COUNT(*) >= 20 THEN '✓ CORRECT'
        WHEN table_name = 'enriched_messages' AND COUNT(*) >= 10 THEN '✓ CORRECT'
        ELSE '✗ INCORRECT'
    END as status
FROM information_schema.columns
WHERE table_name IN ('enriched_chats', 'enriched_messages')
GROUP BY table_name
ORDER BY table_name;

\echo ''

-- =====================================================
-- 6. Verify important columns exist
-- =====================================================

\echo '6. Verifying critical columns...'

-- Enriched chats columns
SELECT
    'enriched_chats' as table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'enriched_chats'
AND column_name IN (
    'id', 'user_id', 'chat_provider_id', 'quality_score',
    'is_work_related', 'theme', 'intent', 'created_at'
)
ORDER BY column_name;

\echo ''

-- Enriched messages columns
SELECT
    'enriched_messages' as table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'enriched_messages'
AND column_name IN (
    'id', 'user_id', 'message_provider_id', 'overall_risk_level',
    'overall_risk_score', 'risk_categories', 'created_at'
)
ORDER BY column_name;

\echo ''

-- =====================================================
-- 7. Check constraints
-- =====================================================

\echo '7. Verifying constraints...'
SELECT
    tc.table_name,
    tc.constraint_name,
    tc.constraint_type,
    CASE
        WHEN tc.constraint_type = 'UNIQUE' THEN '✓ UNIQUE CONSTRAINT'
        WHEN tc.constraint_type = 'FOREIGN KEY' THEN '✓ FOREIGN KEY'
        WHEN tc.constraint_type = 'CHECK' THEN '✓ CHECK CONSTRAINT'
        WHEN tc.constraint_type = 'PRIMARY KEY' THEN '✓ PRIMARY KEY'
        ELSE tc.constraint_type
    END as status
FROM information_schema.table_constraints tc
WHERE tc.table_name IN ('enriched_chats', 'enriched_messages')
ORDER BY tc.table_name, tc.constraint_type, tc.constraint_name;

\echo ''

-- =====================================================
-- 8. Check triggers
-- =====================================================

\echo '8. Verifying triggers...'
SELECT
    event_object_table as table_name,
    trigger_name,
    event_manipulation as event,
    action_timing,
    CASE
        WHEN trigger_name LIKE '%updated_at%' THEN '✓ UPDATE TRIGGER'
        ELSE '✓ TRIGGER EXISTS'
    END as status
FROM information_schema.triggers
WHERE event_object_table IN ('enriched_chats', 'enriched_messages')
ORDER BY event_object_table, trigger_name;

\echo ''

-- =====================================================
-- 9. Test data types for JSONB columns
-- =====================================================

\echo '9. Verifying JSONB columns...'
SELECT
    table_name,
    column_name,
    data_type,
    CASE
        WHEN data_type = 'jsonb' THEN '✓ JSONB'
        WHEN data_type = 'ARRAY' THEN '✓ ARRAY'
        ELSE '✗ WRONG TYPE'
    END as status
FROM information_schema.columns
WHERE table_name IN ('enriched_chats', 'enriched_messages')
AND (data_type = 'jsonb' OR data_type = 'ARRAY')
ORDER BY table_name, column_name;

\echo ''

-- =====================================================
-- 10. Summary
-- =====================================================

\echo '========================================='
\echo 'Migration Verification Summary'
\echo '========================================='

DO $$
DECLARE
    chat_table_exists BOOLEAN;
    message_table_exists BOOLEAN;
    chat_rls_enabled BOOLEAN;
    message_rls_enabled BOOLEAN;
    chat_policies_count INTEGER;
    message_policies_count INTEGER;
    chat_indexes_count INTEGER;
    message_indexes_count INTEGER;
BEGIN
    -- Check tables exist
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'enriched_chats'
    ) INTO chat_table_exists;

    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'enriched_messages'
    ) INTO message_table_exists;

    -- Check RLS
    SELECT rowsecurity INTO chat_rls_enabled
    FROM pg_tables WHERE tablename = 'enriched_chats';

    SELECT rowsecurity INTO message_rls_enabled
    FROM pg_tables WHERE tablename = 'enriched_messages';

    -- Count policies
    SELECT COUNT(*) INTO chat_policies_count
    FROM pg_policies WHERE tablename = 'enriched_chats';

    SELECT COUNT(*) INTO message_policies_count
    FROM pg_policies WHERE tablename = 'enriched_messages';

    -- Count indexes
    SELECT COUNT(*) INTO chat_indexes_count
    FROM pg_indexes WHERE tablename = 'enriched_chats';

    SELECT COUNT(*) INTO message_indexes_count
    FROM pg_indexes WHERE tablename = 'enriched_messages';

    -- Print summary
    RAISE NOTICE '';
    RAISE NOTICE 'Tables:';
    RAISE NOTICE '  enriched_chats: %', CASE WHEN chat_table_exists THEN '✓ EXISTS' ELSE '✗ MISSING' END;
    RAISE NOTICE '  enriched_messages: %', CASE WHEN message_table_exists THEN '✓ EXISTS' ELSE '✗ MISSING' END;
    RAISE NOTICE '';
    RAISE NOTICE 'Row Level Security:';
    RAISE NOTICE '  enriched_chats: %', CASE WHEN chat_rls_enabled THEN '✓ ENABLED' ELSE '✗ DISABLED' END;
    RAISE NOTICE '  enriched_messages: %', CASE WHEN message_rls_enabled THEN '✓ ENABLED' ELSE '✗ DISABLED' END;
    RAISE NOTICE '';
    RAISE NOTICE 'RLS Policies:';
    RAISE NOTICE '  enriched_chats: % policies', chat_policies_count;
    RAISE NOTICE '  enriched_messages: % policies', message_policies_count;
    RAISE NOTICE '';
    RAISE NOTICE 'Indexes:';
    RAISE NOTICE '  enriched_chats: % indexes', chat_indexes_count;
    RAISE NOTICE '  enriched_messages: % indexes', message_indexes_count;
    RAISE NOTICE '';

    IF chat_table_exists AND message_table_exists AND
       chat_rls_enabled AND message_rls_enabled AND
       chat_policies_count >= 4 AND message_policies_count >= 4 THEN
        RAISE NOTICE '✓✓✓ MIGRATION VERIFICATION PASSED ✓✓✓';
        RAISE NOTICE 'All checks completed successfully!';
    ELSE
        RAISE NOTICE '✗✗✗ MIGRATION VERIFICATION FAILED ✗✗✗';
        RAISE NOTICE 'Some checks did not pass. Review the output above.';
    END IF;
    RAISE NOTICE '';
END $$;

\echo '========================================='
