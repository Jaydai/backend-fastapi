#!/bin/bash

# Test script for version slug migration
# This script applies the migration to the database and verifies the results

set -e  # Exit on error

echo "🧪 Testing Version Slug Migration"
echo "=================================="
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    echo "   Please create a .env file with SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY"
    exit 1
fi

# Source environment variables
source .env

# Check required environment variables
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_SERVICE_ROLE_KEY" ]; then
    echo "❌ Error: Required environment variables not set"
    echo "   Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env"
    exit 1
fi

echo "✅ Environment variables loaded"
echo ""

# Extract database connection details from SUPABASE_URL
# Format: https://xxxxx.supabase.co
PROJECT_REF=$(echo $SUPABASE_URL | sed 's/https:\/\///' | sed 's/.supabase.co//')

echo "📋 Migration Plan:"
echo "   1. Apply add_version_slug_column.sql"
echo "   2. Verify slug column exists"
echo "   3. Check sample slugs generated"
echo "   4. Verify unique constraint"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Migration cancelled"
    exit 0
fi

echo ""
echo "🚀 Applying migration..."
echo ""

# Note: This is a placeholder - actual migration needs to be run via Supabase SQL Editor or psql
# The Python client doesn't support raw SQL execution

cat <<EOF
⚠️  MANUAL STEP REQUIRED:

Please apply the migration manually using one of these methods:

METHOD 1: Supabase SQL Editor (Recommended)
   1. Go to https://app.supabase.com/project/${PROJECT_REF}/sql
   2. Copy the contents of migrations/add_version_slug_column.sql
   3. Paste and run the SQL

METHOD 2: psql Command Line
   1. Get your database password from Supabase dashboard
   2. Run: psql -h db.${PROJECT_REF}.supabase.co -U postgres -d postgres -f migrations/add_version_slug_column.sql

After applying the migration, you can verify it with:
   python scripts/verify_version_slug_migration.py

EOF

echo ""
echo "📄 Migration SQL file location:"
echo "   $(pwd)/migrations/add_version_slug_column.sql"
echo ""
