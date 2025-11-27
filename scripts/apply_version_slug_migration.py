#!/usr/bin/env python3
"""
Script to apply the version slug migration and verify the results.

Usage:
    python scripts/apply_version_slug_migration.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import from backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

from supabase import Client, create_client

# Load environment variables
load_dotenv()


def get_supabase_admin_client() -> Client:
    """Get Supabase admin client."""
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url or not service_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")

    return create_client(url, service_key)


def apply_migration(client: Client, migration_file: str) -> None:
    """Apply SQL migration file."""
    migration_path = Path(__file__).parent.parent / "migrations" / migration_file

    if not migration_path.exists():
        raise FileNotFoundError(f"Migration file not found: {migration_path}")

    print(f"📄 Reading migration file: {migration_file}")
    with open(migration_path) as f:
        sql = f.read()

    print("🚀 Applying migration...")
    try:
        # Note: Supabase Python client doesn't support raw SQL execution directly
        # We need to use the REST API or PostgreSQL connection
        # For now, this script will just read and display the SQL
        print("⚠️  This script displays the SQL. Please apply it manually via Supabase SQL Editor or psql.")
        print("\n" + "=" * 80)
        print(sql)
        print("=" * 80 + "\n")
    except Exception as e:
        print(f"❌ Error applying migration: {e}")
        raise


def verify_migration(client: Client) -> None:
    """Verify the migration was applied correctly."""
    print("\n🔍 Verifying migration...")

    try:
        # Check if slug column exists by querying a version
        response = client.table("prompt_templates_versions").select("id, template_id, name, slug").limit(5).execute()

        if not response.data:
            print("⚠️  No versions found in database")
            return

        print(f"✅ Found {len(response.data)} sample versions with slugs:")
        for version in response.data:
            print(f"   - {version['name']}: {version['slug']}")

        # Check for duplicate slugs
        print("\n🔍 Checking for duplicate slugs...")
        response = client.rpc("check_duplicate_version_slugs").execute()

        if response.data and len(response.data) > 0:
            print(f"❌ Found {len(response.data)} duplicate slugs:")
            for dup in response.data:
                print(f"   - {dup}")
        else:
            print("✅ No duplicate slugs found")

    except Exception as e:
        print(f"⚠️  Verification check failed: {e}")


def main():
    """Main execution function."""
    print("🔧 Version Slug Migration Tool\n")

    try:
        # Get admin client
        client = get_supabase_admin_client()
        print("✅ Connected to Supabase\n")

        # Apply migration
        apply_migration(client, "add_version_slug_column.sql")

        # Verify migration
        # verify_migration(client)

        print("\n✅ Migration process complete!")
        print("\n📝 Next steps:")
        print("   1. Copy the SQL above and run it in Supabase SQL Editor")
        print("   2. Run this script again to verify (uncomment verify_migration)")
        print("   3. Proceed to Phase 2: Create DTOs and repository methods")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
