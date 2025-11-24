"""Test improved enrichment by processing actual Supabase data (sample)."""
import argparse
import logging
import os
from typing import Dict, Any, List
from supabase import Client, ClientOptions, create_client
import requests


LOGGER = logging.getLogger(__name__)


def build_client(url: str, key: str) -> Client:
    options = ClientOptions(
        schema="public",
        headers={},
        auto_refresh_token=False,
        persist_session=False,
    )
    return create_client(url, key, options=options)


def fetch_sample_messages(client: Client, limit: int = None) -> List[Dict[str, Any]]:
    """Fetch sample user messages from Supabase"""
    query = (
        client.table("messages")
        .select("*")
        .eq("role", "user")
        .order("created_at", desc=True)
    )

    if limit:
        query = query.limit(limit)

    response = query.execute()
    return response.data or []


def fetch_sample_chats(client: Client, message_rows: List[Dict[str, Any]], limit_chats: int = None) -> List[Dict[str, Any]]:
    """Fetch messages for chat enrichment based on chat_provider_ids"""
    # Get unique chat IDs
    chat_ids = list({m.get("chat_provider_id") for m in message_rows if m.get("chat_provider_id")})

    if not chat_ids:
        LOGGER.warning("No chat_provider_ids found in messages")
        return []

    # Limit chat IDs if specified
    if limit_chats:
        chat_ids = chat_ids[:limit_chats]

    # Fetch all messages for these chats
    response = (
        client.table("messages")
        .select("*")
        .in_("chat_provider_id", chat_ids)
        .order("created_at", desc=False)
        .execute()
    )
    return response.data or []


def group_messages_by_chat(rows: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group messages by chat_provider_id"""
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        chat_id = row.get("chat_provider_id")
        if chat_id:
            if chat_id not in grouped:
                grouped[chat_id] = []
            grouped[chat_id].append(row)
    return grouped


def build_chat_enrichment_items(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build chat enrichment items from messages"""
    grouped = group_messages_by_chat(messages)
    chat_items: List[Dict[str, Any]] = []

    for chat_provider_id, rows in grouped.items():
        # Sort by creation time
        sorted_rows = sorted(rows, key=lambda r: r.get("created_at", ""))

        # Find user and assistant messages
        user_msg = None
        assistant_msg = None

        for row in sorted_rows:
            role = (row.get("role") or "").lower()
            if role == "user" and not user_msg:
                user_msg = row.get("content") or ""
            elif role in ("assistant", "system") and not assistant_msg:
                assistant_msg = row.get("content")

        # Only create item if we have a user message
        if user_msg:
            chat_items.append({
                "user_message": user_msg,
                "assistant_response": assistant_msg,
                "chat_provider_id": chat_provider_id,
                "message_provider_id": sorted_rows[0].get("message_provider_id"),
                "chat_id": sorted_rows[0].get("chat_id"),
                "user_id": sorted_rows[0].get("user_id"),
            })

    return chat_items


def post_json(base_url: str, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """POST JSON to endpoint and return response"""
    url = f"{base_url.rstrip('/')}{path}"
    response = requests.post(url, json=payload, timeout=300)

    if not response.ok:
        raise RuntimeError(f"POST {path} failed ({response.status_code}): {response.text}")

    return response.json()


def test_message_enrichment(base_url: str, messages: List[Dict[str, Any]]) -> None:
    """Test message enrichment with real data"""
    LOGGER.info(f"\n{'='*80}\nTesting MESSAGE ENRICHMENT (RISK ASSESSMENT)\n{'='*80}")

    # Convert to enrichment format
    enrichment_messages = [
        {
            "content": msg.get("content") or "",
            "role": msg.get("role") or "user",
            "message_provider_id": msg.get("message_provider_id"),
            "message_id": msg.get("id"),
            "user_id": msg.get("user_id"),
        }
        for msg in messages
    ]

    LOGGER.info(f"Enriching {len(enrichment_messages)} messages in batches of 100...")

    # Split into batches of 100 (API limit)
    batch_size = 100
    all_results = []

    for i in range(0, len(enrichment_messages), batch_size):
        batch = enrichment_messages[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(enrichment_messages) + batch_size - 1) // batch_size

        LOGGER.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} messages)...")

        payload = {"messages": batch}
        result = post_json(base_url, "/enrichment/enrich-message-batch", payload)
        all_results.extend(result.get("results", []))

    # Process results
    success_count = sum(1 for r in all_results if r.get("success"))
    error_count = len(all_results) - success_count

    LOGGER.info(f"\n--- RESULTS ---")
    LOGGER.info(f"Total: {len(all_results)}, Success: {success_count}, Errors: {error_count}")

    # Show sample results
    for i, result_item in enumerate(all_results[:3]):  # Show first 3
        if result_item.get("success"):
            data = result_item.get("data", {})
            LOGGER.info(f"\n[{i+1}] Message: {enrichment_messages[i]['message_provider_id']}")
            LOGGER.info(f"  Risk Level: {data.get('overall_risk_level')} (score: {data.get('overall_risk_score')})")
            LOGGER.info(f"  Confidence: {data.get('overall_confidence')}%")
            LOGGER.info(f"  Action: {data.get('suggested_action')}")

            # Show detected risks
            detected = [cat for cat, details in data.get('risk_categories', {}).items()
                       if isinstance(details, dict) and details.get('detected')]
            if detected:
                LOGGER.info(f"  Detected: {', '.join(detected)}")
        else:
            LOGGER.error(f"\n[{i+1}] FAILED: {result_item.get('error')}")

    if error_count > 0:
        LOGGER.warning(f"\n⚠️  {error_count} messages failed to enrich")


def test_chat_enrichment(base_url: str, chats: List[Dict[str, Any]]) -> None:
    """Test chat enrichment with real data"""
    LOGGER.info(f"\n{'='*80}\nTesting CHAT ENRICHMENT (CLASSIFICATION + QUALITY)\n{'='*80}")

    LOGGER.info(f"Enriching {len(chats)} chats in batches of 50...")

    # Split into batches of 50 (API limit)
    batch_size = 50
    all_results = []

    for i in range(0, len(chats), batch_size):
        batch = chats[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(chats) + batch_size - 1) // batch_size

        LOGGER.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} chats)...")

        payload = {"chats": batch}
        result = post_json(base_url, "/enrichment/enrich-chat-batch", payload)
        all_results.extend(result.get("results", []))

    # Process results
    success_count = sum(1 for r in all_results if r.get("success"))
    error_count = len(all_results) - success_count

    LOGGER.info(f"\n--- RESULTS ---")
    LOGGER.info(f"Total: {len(all_results)}, Success: {success_count}, Errors: {error_count}")

    # Show sample results
    for i, result_item in enumerate(all_results[:3]):  # Show first 3
        if result_item.get("success"):
            data = result_item.get("data", {})
            LOGGER.info(f"\n[{i+1}] Chat: {chats[i]['chat_provider_id']}")
            LOGGER.info(f"  Work Related: {data.get('is_work_related')}")
            LOGGER.info(f"  Theme: {data.get('theme')}")
            LOGGER.info(f"  Intent: {data.get('intent')}")
            LOGGER.info(f"  Skill Level: {data.get('skill_level')}")

            quality = data.get('quality', {})
            if quality:
                LOGGER.info(f"  Quality Score: {quality.get('quality_score')}/100")
                LOGGER.info(f"  Clarity: {quality.get('clarity_score')}/5")
                LOGGER.info(f"  Specificity: {quality.get('specificity_score')}/5")

            domain = data.get('domain_expertise', {})
            if domain and domain.get('tech_stack'):
                LOGGER.info(f"  Tech Stack: {', '.join(domain.get('tech_stack', [])[:3])}")
        else:
            LOGGER.error(f"\n[{i+1}] FAILED: {result_item.get('error')}")

    if error_count > 0:
        LOGGER.warning(f"\n⚠️  {error_count} chats failed to enrich")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(message)s"
    )

    parser = argparse.ArgumentParser(description="Test improved enrichment with real Supabase data")
    parser.add_argument("--supabase-url", help="Supabase project URL (or set SUPABASE_URL env)")
    parser.add_argument("--supabase-key", help="Supabase service key (or set SUPABASE_KEY env)")
    parser.add_argument("--api-base-url", default="http://localhost:8000", help="Base URL for enrichment API")
    parser.add_argument("--limit", type=int, default=None, help="Number of sample messages to test (default: all)")
    parser.add_argument("--limit-chats", type=int, default=None, help="Number of chats to test (default: all)")
    parser.add_argument("--test-messages", action="store_true", help="Test message enrichment only")
    parser.add_argument("--test-chats", action="store_true", help="Test chat enrichment only")
    args = parser.parse_args()

    # Get Supabase credentials
    supabase_url = args.supabase_url or os.getenv("SUPABASE_URL")
    supabase_key = args.supabase_key or os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        LOGGER.error("Supabase credentials required. Provide --supabase-url and --supabase-key or set env vars")
        return

    # Connect to Supabase
    LOGGER.info(f"Connecting to Supabase...")
    client = build_client(supabase_url, supabase_key)

    # Fetch sample data
    if args.limit:
        LOGGER.info(f"Fetching {args.limit} sample messages...")
    else:
        LOGGER.info(f"Fetching ALL messages...")

    messages = fetch_sample_messages(client, args.limit)

    if not messages:
        LOGGER.error("No messages found in Supabase")
        return

    LOGGER.info(f"Found {len(messages)} messages")

    # Test message enrichment
    if not args.test_chats:
        test_message_enrichment(args.api_base_url, messages)

    # Test chat enrichment
    if not args.test_messages:
        LOGGER.info(f"\nFetching messages for chat enrichment...")
        chat_messages = fetch_sample_chats(client, messages, args.limit_chats)
        chat_items = build_chat_enrichment_items(chat_messages)

        if chat_items:
            LOGGER.info(f"Built {len(chat_items)} chat items")
            test_chat_enrichment(args.api_base_url, chat_items)
        else:
            LOGGER.warning("No chat items to enrich")

    LOGGER.info(f"\n{'='*80}\nTESTING COMPLETE\n{'='*80}")


if __name__ == "__main__":
    main()
