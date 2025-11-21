-- =====================================================
-- Rollback Enrichment Tables Migration
-- Drops all enrichment-related tables, indexes, and policies
-- =====================================================

-- WARNING: This will delete all data in enriched_chats and enriched_messages tables
-- Make sure to backup data before running this script!

-- =====================================================
-- Drop RLS Policies
-- =====================================================

-- Drop enriched_chats policies
DROP POLICY IF EXISTS "Users can view their own enriched chats" ON enriched_chats;
DROP POLICY IF EXISTS "Users can insert their own enriched chats" ON enriched_chats;
DROP POLICY IF EXISTS "Users can update their own enriched chats" ON enriched_chats;
DROP POLICY IF EXISTS "Users can delete their own enriched chats" ON enriched_chats;

-- Drop enriched_messages policies
DROP POLICY IF EXISTS "Users can view their own enriched messages" ON enriched_messages;
DROP POLICY IF EXISTS "Users can insert their own enriched messages" ON enriched_messages;
DROP POLICY IF EXISTS "Users can update their own enriched messages" ON enriched_messages;
DROP POLICY IF EXISTS "Users can delete their own enriched messages" ON enriched_messages;

-- =====================================================
-- Drop Triggers
-- =====================================================

DROP TRIGGER IF EXISTS update_enriched_chats_updated_at ON enriched_chats;
DROP TRIGGER IF EXISTS update_enriched_messages_updated_at ON enriched_messages;

-- =====================================================
-- Drop Indexes (explicitly, though CASCADE will handle them)
-- =====================================================

-- Enriched chats indexes
DROP INDEX IF EXISTS idx_enriched_chats_user_id;
DROP INDEX IF EXISTS idx_enriched_chats_chat_provider_id;
DROP INDEX IF EXISTS idx_enriched_chats_created_at;
DROP INDEX IF EXISTS idx_enriched_chats_quality_score;
DROP INDEX IF EXISTS idx_enriched_chats_work_related;
DROP INDEX IF EXISTS idx_enriched_chats_theme;
DROP INDEX IF EXISTS idx_enriched_chats_intent;

-- Enriched messages indexes
DROP INDEX IF EXISTS idx_enriched_messages_user_id;
DROP INDEX IF EXISTS idx_enriched_messages_provider_id;
DROP INDEX IF EXISTS idx_enriched_messages_created_at;
DROP INDEX IF EXISTS idx_enriched_messages_risk_level;
DROP INDEX IF EXISTS idx_enriched_messages_risk_score;
DROP INDEX IF EXISTS idx_enriched_messages_whitelist;
DROP INDEX IF EXISTS idx_enriched_messages_risk_categories;
DROP INDEX IF EXISTS idx_enriched_messages_detected_issues;

-- =====================================================
-- Drop Tables
-- =====================================================

DROP TABLE IF EXISTS enriched_messages CASCADE;
DROP TABLE IF EXISTS enriched_chats CASCADE;

-- =====================================================
-- Drop Functions (only if not used elsewhere)
-- =====================================================

-- Note: update_updated_at_column() function might be used by other tables
-- Only drop if you're sure it's not needed elsewhere
-- DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- =====================================================
-- Rollback Complete
-- =====================================================

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name IN ('enriched_chats', 'enriched_messages')
    ) THEN
        RAISE NOTICE 'Rollback completed successfully! Tables enriched_chats and enriched_messages have been removed.';
    ELSE
        RAISE EXCEPTION 'Rollback failed - tables still exist';
    END IF;
END $$;
