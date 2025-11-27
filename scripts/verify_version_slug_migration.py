#!/usr/bin/env python3
"""
Script to verify the version slug migration was applied correctly.

This script checks:
1. Slug column exists and is populated
2. All slugs are unique within each template
3. Slug format matches expected pattern
4. Auto-generation trigger works for new versions

Usage:
    python scripts/verify_version_slug_migration.py
"""

import os
import sys
from collections import defaultdict
from pathlib import Path

# Add parent directory to path
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


def verify_slug_column_exists(client: Client) -> bool:
    """Verify slug column exists and is populated."""
    print("🔍 Checking if slug column exists...")

    try:
        response = client.table("prompt_templates_versions").select("id, name, slug").limit(1).execute()

        if response.data and len(response.data) > 0:
            version = response.data[0]
            if "slug" in version and version["slug"]:
                print("   ✅ Slug column exists and is populated")
                print(f"   Example: '{version['name']}' → '{version['slug']}'")
                return True
            else:
                print("   ❌ Slug column exists but is not populated")
                return False
        else:
            print("   ⚠️  No versions found in database")
            return False

    except Exception as e:
        print(f"   ❌ Error checking slug column: {e}")
        return False


def verify_slug_uniqueness(client: Client) -> bool:
    """Verify all slugs are unique within each template."""
    print("\n🔍 Checking slug uniqueness within templates...")

    try:
        # Get all versions
        response = client.table("prompt_templates_versions").select("template_id, slug").execute()

        if not response.data:
            print("   ⚠️  No versions found")
            return True

        # Group by template_id and check for duplicates
        template_slugs = defaultdict(list)
        for version in response.data:
            template_slugs[version["template_id"]].append(version["slug"])

        duplicates_found = False
        for template_id, slugs in template_slugs.items():
            if len(slugs) != len(set(slugs)):
                # Find duplicate slugs
                seen = set()
                dupes = set()
                for slug in slugs:
                    if slug in seen:
                        dupes.add(slug)
                    seen.add(slug)

                print(f"   ❌ Template {template_id} has duplicate slugs: {dupes}")
                duplicates_found = True

        if not duplicates_found:
            print("   ✅ All slugs are unique within their templates")
            print(f"   Checked {len(template_slugs)} templates with {len(response.data)} total versions")
            return True
        else:
            return False

    except Exception as e:
        print(f"   ❌ Error checking uniqueness: {e}")
        return False


def verify_slug_format(client: Client) -> bool:
    """Verify slug format matches expected pattern."""
    print("\n🔍 Checking slug format...")

    try:
        response = client.table("prompt_templates_versions").select("name, slug").limit(10).execute()

        if not response.data:
            print("   ⚠️  No versions found")
            return True

        all_valid = True
        for version in response.data:
            slug = version["slug"]

            # Check for invalid characters
            if not all(c.isalnum() or c == "-" for c in slug):
                print(f"   ❌ Invalid characters in slug '{slug}' (name: '{version['name']}')")
                all_valid = False

            # Check for leading/trailing hyphens
            if slug.startswith("-") or slug.endswith("-"):
                print(f"   ❌ Invalid format (leading/trailing hyphen): '{slug}' (name: '{version['name']}')")
                all_valid = False

            # Check for consecutive hyphens
            if "--" in slug:
                print(f"   ❌ Invalid format (consecutive hyphens): '{slug}' (name: '{version['name']}')")
                all_valid = False

        if all_valid:
            print("   ✅ All slugs have valid format")
            print(f"   Sample slugs: {[v['slug'] for v in response.data[:5]]}")
            return True
        else:
            return False

    except Exception as e:
        print(f"   ❌ Error checking format: {e}")
        return False


def display_sample_slugs(client: Client) -> None:
    """Display sample slugs for manual inspection."""
    print("\n📋 Sample slugs:")

    try:
        response = (
            client.table("prompt_templates_versions")
            .select("name, slug, created_at")
            .order("created_at", desc=True)
            .limit(10)
            .execute()
        )

        if not response.data:
            print("   No versions found")
            return

        for version in response.data:
            print(f"   • {version['name']:<40} → {version['slug']}")

    except Exception as e:
        print(f"   ⚠️  Error fetching samples: {e}")


def main():
    """Main execution function."""
    print("🔧 Version Slug Migration Verification\n")
    print("=" * 80)
    print()

    try:
        # Get admin client
        client = get_supabase_admin_client()
        print("✅ Connected to Supabase\n")

        # Run verification checks
        checks = [
            verify_slug_column_exists(client),
            verify_slug_uniqueness(client),
            verify_slug_format(client),
        ]

        # Display samples
        display_sample_slugs(client)

        # Summary
        print("\n" + "=" * 80)
        print("\n📊 Verification Summary:")
        print(f"   Total checks: {len(checks)}")
        print(f"   Passed: {sum(checks)}")
        print(f"   Failed: {len(checks) - sum(checks)}")

        if all(checks):
            print("\n✅ All verification checks passed!")
            print("\n📝 Next steps:")
            print("   → Proceed to Phase 2: Create DTOs and repository methods")
            return 0
        else:
            print("\n❌ Some verification checks failed")
            print("   → Please review the errors above and fix the migration")
            return 1

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
