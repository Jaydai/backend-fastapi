-- =====================================================
-- Enrichment Tables Migration
-- Creates tables for chat classification and message risk assessment
-- =====================================================

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- Table: enriched_chats
-- Stores chat classification and quality assessment data
-- =====================================================

CREATE TABLE IF NOT EXISTS enriched_chats (
    -- Primary key and timestamps
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- User and chat references
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    chat_id BIGINT,
    chat_provider_id TEXT NOT NULL,
    message_provider_id TEXT,

    -- Classification results
    is_work_related BOOLEAN NOT NULL DEFAULT FALSE,
    theme TEXT,
    intent TEXT,

    -- Quality metrics (0-100 for quality_score, 0-5 for others)
    quality_score INTEGER CHECK (quality_score >= 0 AND quality_score <= 100),
    clarity_score INTEGER CHECK (clarity_score >= 0 AND clarity_score <= 5),
    context_score INTEGER CHECK (context_score >= 0 AND context_score <= 5),
    specificity_score INTEGER CHECK (specificity_score >= 0 AND specificity_score <= 5),
    actionability_score INTEGER CHECK (actionability_score >= 0 AND actionability_score <= 5),

    -- Feedback details
    feedback_summary TEXT,
    feedback_strengths TEXT[],
    feedback_improvements TEXT[],
    improved_prompt_example TEXT,

    -- User overrides
    user_override_quality BOOLEAN NOT NULL DEFAULT FALSE,
    user_quality_score INTEGER CHECK (user_quality_score >= 0 AND user_quality_score <= 100),

    -- Processing metadata
    raw_response JSONB,
    processing_time_ms INTEGER,
    model_used TEXT,

    -- Constraints
    CONSTRAINT unique_user_chat_provider UNIQUE (user_id, chat_provider_id)
);

-- =====================================================
-- Table: enriched_messages
-- Stores message risk assessment data
-- =====================================================

CREATE TABLE IF NOT EXISTS enriched_messages (
    -- Primary key and timestamps
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- User and message references
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    message_id BIGINT,
    message_provider_id TEXT NOT NULL,

    -- Overall risk assessment
    overall_risk_level TEXT NOT NULL DEFAULT 'none'
        CHECK (overall_risk_level IN ('none', 'low', 'medium', 'high', 'critical')),
    overall_risk_score NUMERIC(5,2) NOT NULL DEFAULT 0.0
        CHECK (overall_risk_score >= 0 AND overall_risk_score <= 100),

    -- Risk categories (JSON object with category details)
    -- Structure: { "pii": { "level": "high", "score": 85.5, "detected": true, "details": "..." }, ... }
    risk_categories JSONB NOT NULL DEFAULT '{}'::jsonb,

    -- Risk summary (array of risk description strings)
    risk_summary TEXT[] NOT NULL DEFAULT '{}',

    -- Detected issues (JSON array of issue objects)
    -- Structure: [{ "category": "pii", "severity": "high", "description": "...", "details": {...} }, ...]
    detected_issues JSONB NOT NULL DEFAULT '[]'::jsonb,

    -- User whitelist flag
    user_whitelist BOOLEAN NOT NULL DEFAULT FALSE,

    -- Processing metadata
    processing_time_ms INTEGER,
    model_used TEXT,

    -- Constraints
    CONSTRAINT unique_user_message_provider UNIQUE (user_id, message_provider_id)
);

-- =====================================================
-- Indexes for Performance
-- =====================================================

-- Enriched chats indexes
CREATE INDEX IF NOT EXISTS idx_enriched_chats_user_id ON enriched_chats(user_id);
CREATE INDEX IF NOT EXISTS idx_enriched_chats_chat_provider_id ON enriched_chats(chat_provider_id);
CREATE INDEX IF NOT EXISTS idx_enriched_chats_created_at ON enriched_chats(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_enriched_chats_quality_score ON enriched_chats(quality_score DESC) WHERE quality_score IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_enriched_chats_work_related ON enriched_chats(is_work_related);
CREATE INDEX IF NOT EXISTS idx_enriched_chats_theme ON enriched_chats(theme);
CREATE INDEX IF NOT EXISTS idx_enriched_chats_intent ON enriched_chats(intent);

-- Enriched messages indexes
CREATE INDEX IF NOT EXISTS idx_enriched_messages_user_id ON enriched_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_enriched_messages_provider_id ON enriched_messages(message_provider_id);
CREATE INDEX IF NOT EXISTS idx_enriched_messages_created_at ON enriched_messages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_enriched_messages_risk_level ON enriched_messages(overall_risk_level);
CREATE INDEX IF NOT EXISTS idx_enriched_messages_risk_score ON enriched_messages(overall_risk_score DESC);
CREATE INDEX IF NOT EXISTS idx_enriched_messages_whitelist ON enriched_messages(user_whitelist);

-- GIN indexes for JSONB columns (for better query performance on JSON data)
CREATE INDEX IF NOT EXISTS idx_enriched_messages_risk_categories ON enriched_messages USING GIN (risk_categories);
CREATE INDEX IF NOT EXISTS idx_enriched_messages_detected_issues ON enriched_messages USING GIN (detected_issues);

-- =====================================================
-- Row Level Security (RLS) Policies
-- =====================================================

-- Enable RLS on both tables
ALTER TABLE enriched_chats ENABLE ROW LEVEL SECURITY;
ALTER TABLE enriched_messages ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Users can view their own enriched chats" ON enriched_chats;
DROP POLICY IF EXISTS "Users can insert their own enriched chats" ON enriched_chats;
DROP POLICY IF EXISTS "Users can update their own enriched chats" ON enriched_chats;
DROP POLICY IF EXISTS "Users can delete their own enriched chats" ON enriched_chats;

DROP POLICY IF EXISTS "Users can view their own enriched messages" ON enriched_messages;
DROP POLICY IF EXISTS "Users can insert their own enriched messages" ON enriched_messages;
DROP POLICY IF EXISTS "Users can update their own enriched messages" ON enriched_messages;
DROP POLICY IF EXISTS "Users can delete their own enriched messages" ON enriched_messages;

-- Enriched chats RLS policies
CREATE POLICY "Users can view their own enriched chats"
    ON enriched_chats FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own enriched chats"
    ON enriched_chats FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own enriched chats"
    ON enriched_chats FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own enriched chats"
    ON enriched_chats FOR DELETE
    USING (auth.uid() = user_id);

-- Enriched messages RLS policies
CREATE POLICY "Users can view their own enriched messages"
    ON enriched_messages FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own enriched messages"
    ON enriched_messages FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own enriched messages"
    ON enriched_messages FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own enriched messages"
    ON enriched_messages FOR DELETE
    USING (auth.uid() = user_id);

-- =====================================================
-- Triggers for updated_at timestamps
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for enriched_chats
DROP TRIGGER IF EXISTS update_enriched_chats_updated_at ON enriched_chats;
CREATE TRIGGER update_enriched_chats_updated_at
    BEFORE UPDATE ON enriched_chats
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for enriched_messages
DROP TRIGGER IF EXISTS update_enriched_messages_updated_at ON enriched_messages;
CREATE TRIGGER update_enriched_messages_updated_at
    BEFORE UPDATE ON enriched_messages
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- Comments for documentation
-- =====================================================

COMMENT ON TABLE enriched_chats IS 'Stores AI-powered chat classification and quality assessment data';
COMMENT ON TABLE enriched_messages IS 'Stores AI-powered message risk assessment data';

COMMENT ON COLUMN enriched_chats.quality_score IS 'Overall quality score from 0-100';
COMMENT ON COLUMN enriched_chats.clarity_score IS 'Clarity score from 0-5';
COMMENT ON COLUMN enriched_chats.context_score IS 'Context score from 0-5';
COMMENT ON COLUMN enriched_chats.specificity_score IS 'Specificity score from 0-5';
COMMENT ON COLUMN enriched_chats.actionability_score IS 'Actionability score from 0-5';
COMMENT ON COLUMN enriched_chats.user_override_quality IS 'Whether user has manually overridden the quality score';

COMMENT ON COLUMN enriched_messages.overall_risk_level IS 'Overall risk level: none, low, medium, high, critical';
COMMENT ON COLUMN enriched_messages.overall_risk_score IS 'Overall risk score from 0-100';
COMMENT ON COLUMN enriched_messages.risk_categories IS 'JSONB object containing detailed risk assessment for each category (pii, security, confidential, misinformation, data_leakage, compliance)';
COMMENT ON COLUMN enriched_messages.detected_issues IS 'JSONB array of detected risk issues with category, severity, description, and details';
COMMENT ON COLUMN enriched_messages.user_whitelist IS 'Whether user has whitelisted this message to ignore risk warnings';

-- =====================================================
-- Grant permissions (if needed for service role)
-- =====================================================

-- Grant usage on sequences
GRANT USAGE ON SEQUENCE enriched_chats_id_seq TO authenticated;
GRANT USAGE ON SEQUENCE enriched_messages_id_seq TO authenticated;

-- =====================================================
-- Migration Complete
-- =====================================================

-- Verify tables were created
DO $$
BEGIN
    IF EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name IN ('enriched_chats', 'enriched_messages')
    ) THEN
        RAISE NOTICE 'Migration completed successfully! Tables: enriched_chats, enriched_messages';
    ELSE
        RAISE EXCEPTION 'Migration failed - tables not created';
    END IF;
END $$;
