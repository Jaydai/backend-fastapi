-- Migration: Create users_onboarding table
-- This table stores onboarding flow state separate from users_metadata
-- Run this in Supabase SQL Editor or via migrations

-- Create the users_onboarding table
CREATE TABLE IF NOT EXISTS users_onboarding (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Flow state
    flow_type TEXT CHECK (flow_type IN ('invited', 'create_org', 'personal')),
    current_step TEXT NOT NULL DEFAULT 'not_started' CHECK (current_step IN (
        'not_started', 'flow_selection', 'org_details', 'org_billing', 'org_invite',
        'personal_questions', 'personal_chat', 'workspace_ready', 'extension_check', 'completed'
    )),
    completed_at TIMESTAMPTZ,
    dismissed_at TIMESTAMPTZ,

    -- Organization info (collected during onboarding)
    organization_name TEXT,
    organization_description TEXT,
    organization_logo_url TEXT,
    industry TEXT,

    -- User professional info
    job_title TEXT,
    job_description TEXT,
    job_seniority TEXT,

    -- Generated blocks (stored as JSONB)
    context_block JSONB,
    role_blocks JSONB DEFAULT '[]'::jsonb,
    goal_blocks JSONB DEFAULT '[]'::jsonb,
    selected_role_block_ids TEXT[] DEFAULT '{}',
    selected_goal_block_ids TEXT[] DEFAULT '{}',

    -- Use cases
    generated_use_cases JSONB DEFAULT '[]'::jsonb,
    selected_use_cases TEXT[] DEFAULT '{}',

    -- Additional data
    ai_dreams TEXT,
    signup_source TEXT,
    chat_history JSONB,
    chat_summary TEXT,

    -- Extension
    extension_installed BOOLEAN DEFAULT FALSE,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index on user_id for fast lookups
CREATE INDEX IF NOT EXISTS idx_users_onboarding_user_id ON users_onboarding(user_id);

-- Create index on current_step for analytics
CREATE INDEX IF NOT EXISTS idx_users_onboarding_current_step ON users_onboarding(current_step);

-- Enable Row Level Security
ALTER TABLE users_onboarding ENABLE ROW LEVEL SECURITY;

-- Policy: Users can read their own onboarding data
CREATE POLICY "Users can read own onboarding"
    ON users_onboarding
    FOR SELECT
    TO authenticated
    USING (auth.uid() = user_id);

-- Policy: Users can insert their own onboarding data
CREATE POLICY "Users can insert own onboarding"
    ON users_onboarding
    FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

-- Policy: Users can update their own onboarding data
CREATE POLICY "Users can update own onboarding"
    ON users_onboarding
    FOR UPDATE
    TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_users_onboarding_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_users_onboarding_updated_at ON users_onboarding;
CREATE TRIGGER trigger_users_onboarding_updated_at
    BEFORE UPDATE ON users_onboarding
    FOR EACH ROW
    EXECUTE FUNCTION update_users_onboarding_updated_at();

-- Grant permissions to authenticated users
GRANT SELECT, INSERT, UPDATE ON users_onboarding TO authenticated;
