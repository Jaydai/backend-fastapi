import uuid
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient


class TestStatsEndpoints:
    def request(self, method, *args, **kwargs):
        """Helper to automatically include cookies in all requests"""
        if hasattr(self, "cookies"):
            kwargs.setdefault("cookies", self.cookies)
        return getattr(self.client, method)(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.request("get", *args, **kwargs)

    @pytest.fixture(autouse=True)
    def setup(self, test_client, supabase_admin, create_test_user, create_test_organization):
        self.user_id, access_token = create_test_user()
        self.org_id = create_test_organization()

        self.client = test_client
        self.cookies = {"access_token": access_token}
        self.supabase_admin = supabase_admin

        # Create some test chats and messages for stats
        self.test_chats = []
        self.test_messages = []

        # Create test data
        try:
            # Create 3 test chats
            for i in range(3):
                chat_data = {
                    "user_id": self.user_id,
                    "chat_provider_id": f"test-chat-{uuid.uuid4()}",
                    "provider_name": "OpenAI" if i < 2 else "Anthropic",
                    "title": f"Test Chat {i + 1}",
                    "created_at": (datetime.now() - timedelta(days=i)).isoformat(),
                }
                # Model is stored on messages, not chats
                test_model = "gpt-4" if i < 2 else "claude-3-sonnet"
                chat_response = supabase_admin.table("chats").insert(chat_data).execute()
                if chat_response.data:
                    self.test_chats.append(chat_response.data[0])

            # Create test messages for each chat
            for i, chat in enumerate(self.test_chats):
                # Get model based on provider_name
                test_model = "gpt-4" if i < 2 else "claude-3-sonnet"
                for j in range(3):
                    # User message
                    user_msg_data = {
                        "user_id": self.user_id,
                        "chat_provider_id": chat["chat_provider_id"],
                        "message_provider_id": f"test-msg-user-{uuid.uuid4()}",
                        "role": "user",
                        "content": f"Test user message {j + 1} in chat {i + 1}",
                        "model": test_model,
                        "created_at": (datetime.now() - timedelta(days=i, hours=j * 2)).isoformat(),
                    }
                    user_msg_response = supabase_admin.table("messages").insert(user_msg_data).execute()
                    if user_msg_response.data:
                        self.test_messages.append(user_msg_response.data[0])

                        # Assistant message
                        assistant_msg_data = {
                            "user_id": self.user_id,
                            "chat_provider_id": chat["chat_provider_id"],
                            "message_provider_id": f"test-msg-assistant-{uuid.uuid4()}",
                            "parent_message_provider_id": user_msg_response.data[0]["message_provider_id"],
                            "role": "assistant",
                            "content": f"Test assistant response {j + 1} in chat {i + 1}",
                            "model": test_model,
                            "created_at": (datetime.now() - timedelta(days=i, hours=j * 2, seconds=30)).isoformat(),
                        }
                        assistant_msg_response = supabase_admin.table("messages").insert(assistant_msg_data).execute()
                        if assistant_msg_response.data:
                            self.test_messages.append(assistant_msg_response.data[0])

        except Exception as e:
            print(f"Warning creating test data: {e}")

        yield

        # Cleanup test data
        try:
            # Delete messages first (foreign key constraint)
            for msg in self.test_messages:
                supabase_admin.table("messages").delete().eq("id", msg["id"]).execute()

            # Delete chats
            for chat in self.test_chats:
                supabase_admin.table("chats").delete().eq("id", chat["id"]).execute()

        except Exception as e:
            print(f"Cleanup warning: {e}")

    def test_get_user_stats_success(self):
        response = self.get("/user/stats")

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert "total_chats" in data
        assert "recent_chats" in data
        assert "total_messages" in data
        assert "avg_messages_per_chat" in data
        assert "messages_per_day" in data
        assert "chats_per_day" in data
        assert "token_usage" in data
        assert "energy_usage" in data
        assert "thinking_time" in data
        assert "efficiency" in data
        assert "model_usage" in data

        # Check token_usage structure
        assert "recent" in data["token_usage"]
        assert "total" in data["token_usage"]

        # Check energy_usage structure
        assert "total_wh" in data["energy_usage"]
        assert "equivalent" in data["energy_usage"]

        # Data should include our test data
        assert data["total_chats"] >= 3
        assert data["total_messages"] >= 18  # 3 chats * 3 pairs * 2 messages

    def test_get_user_stats_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.get("/user/stats")
        assert response.status_code in [401, 403]

    def test_get_weekly_chat_stats_success(self):
        response = self.get("/user/stats/chats/weekly")

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert "total_conversations" in data
        assert "total_messages" in data
        assert "daily_breakdown" in data

        # Check daily_breakdown structure
        assert isinstance(data["daily_breakdown"], list)
        if len(data["daily_breakdown"]) > 0:
            day = data["daily_breakdown"][0]
            assert "date" in day
            assert "conversations" in day
            assert "messages" in day

    def test_get_weekly_chat_stats_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.get("/user/stats/chats/weekly")
        assert response.status_code in [401, 403]

    def test_get_message_distribution_success(self):
        response = self.get("/user/stats/messages/distribution")

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert "by_role" in data
        assert "by_model" in data
        assert "total_messages" in data

        # Check that we have user and assistant messages
        assert isinstance(data["by_role"], dict)
        assert isinstance(data["by_model"], dict)

        # Should have test data
        if data["total_messages"] > 0:
            assert "user" in data["by_role"] or "assistant" in data["by_role"]

    def test_get_message_distribution_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.get("/user/stats/messages/distribution")
        assert response.status_code in [401, 403]


class TestUsageEndpoints:
    def request(self, method, *args, **kwargs):
        """Helper to automatically include cookies in all requests"""
        if hasattr(self, "cookies"):
            kwargs.setdefault("cookies", self.cookies)
        return getattr(self.client, method)(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.request("get", *args, **kwargs)

    @pytest.fixture(autouse=True)
    def setup(self, test_client, supabase_admin, create_test_user, create_test_organization):
        self.user_id, access_token = create_test_user()
        self.org_id = create_test_organization()

        self.client = test_client
        self.cookies = {"access_token": access_token}
        self.supabase_admin = supabase_admin

        # Create some test chats and messages for usage analytics
        self.test_chats = []
        self.test_messages = []

        try:
            # Create test chat
            chat_data = {
                "user_id": self.user_id,
                "chat_provider_id": f"usage-test-chat-{uuid.uuid4()}",
                "provider_name": "OpenAI",
                "title": "Usage Test Chat",
                "created_at": datetime.now().isoformat(),
            }
            test_model = "gpt-4"  # Model is stored on messages, not chats
            chat_response = supabase_admin.table("chats").insert(chat_data).execute()
            if chat_response.data:
                self.test_chats.append(chat_response.data[0])

                # Create a few messages
                for i in range(2):
                    user_msg_data = {
                        "user_id": self.user_id,
                        "chat_provider_id": chat_response.data[0]["chat_provider_id"],
                        "message_provider_id": f"usage-msg-user-{uuid.uuid4()}",
                        "role": "user",
                        "content": "Test message for usage analytics",
                        "model": test_model,
                        "created_at": (datetime.now() - timedelta(hours=i)).isoformat(),
                    }
                    user_response = supabase_admin.table("messages").insert(user_msg_data).execute()
                    if user_response.data:
                        self.test_messages.append(user_response.data[0])

        except Exception as e:
            print(f"Warning creating test data: {e}")

        yield

        # Cleanup
        try:
            for msg in self.test_messages:
                supabase_admin.table("messages").delete().eq("id", msg["id"]).execute()
            for chat in self.test_chats:
                supabase_admin.table("chats").delete().eq("id", chat["id"]).execute()
        except Exception as e:
            print(f"Cleanup warning: {e}")

    def test_get_usage_overview_success(self):
        response = self.get("/user/usage/overview?days=30")

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert "period" in data
        assert "summary" in data
        assert "model_breakdown" in data
        assert "provider_breakdown" in data
        assert "chat_statistics" in data

        # Check period structure
        assert "days" in data["period"]
        assert "start_date" in data["period"]
        assert "end_date" in data["period"]

        # Check summary structure
        summary = data["summary"]
        assert "total_messages" in summary
        assert "total_chats" in summary
        assert "total_tokens" in summary
        assert "input_tokens" in summary
        assert "output_tokens" in summary
        assert "estimated_cost_usd" in summary
        assert "energy_consumption_wh" in summary
        assert "co2_emissions_kg" in summary
        assert "avg_messages_per_chat" in summary
        assert "top_providers" in summary

        # Check chat_statistics structure
        chat_stats = data["chat_statistics"]
        assert "total_chats" in chat_stats
        assert "avg_messages_per_chat" in chat_stats
        assert "chat_distribution_by_provider" in chat_stats
        assert "recent_chats" in chat_stats

    def test_get_usage_overview_custom_days(self):
        response = self.get("/user/usage/overview?days=7")

        assert response.status_code == 200
        data = response.json()
        assert data["period"]["days"] == 7

    def test_get_usage_overview_invalid_days(self):
        response = self.get("/user/usage/overview?days=500")  # Max is 365
        # Should either reject or cap to 365
        assert response.status_code in [200, 422]

    def test_get_usage_overview_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.get("/user/usage/overview")
        assert response.status_code in [401, 403]

    def test_get_usage_timeline_daily(self):
        response = self.get("/user/usage/timeline?days=7&granularity=daily")

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert "granularity" in data
        assert "period" in data
        assert "timeline" in data

        assert data["granularity"] == "daily"
        assert isinstance(data["timeline"], list)

        # Check timeline data point structure if we have data
        if len(data["timeline"]) > 0:
            point = data["timeline"][0]
            assert "timestamp" in point
            assert "messages" in point
            assert "chats" in point
            assert "input_tokens" in point
            assert "output_tokens" in point
            assert "total_tokens" in point
            assert "cost_usd" in point
            assert "energy_wh" in point

    def test_get_usage_timeline_weekly(self):
        response = self.get("/user/usage/timeline?days=30&granularity=weekly")

        assert response.status_code == 200
        data = response.json()
        assert data["granularity"] == "weekly"

    def test_get_usage_timeline_hourly(self):
        response = self.get("/user/usage/timeline?days=3&granularity=hourly")

        assert response.status_code == 200
        data = response.json()
        assert data["granularity"] == "hourly"

    def test_get_usage_timeline_invalid_granularity(self):
        response = self.get("/user/usage/timeline?granularity=monthly")
        # Should reject invalid granularity
        assert response.status_code == 422

    def test_get_usage_timeline_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.get("/user/usage/timeline")
        assert response.status_code in [401, 403]

    def test_get_usage_patterns_success(self):
        response = self.get("/user/usage/patterns?days=30")

        assert response.status_code == 200
        data = response.json()

        # Check required fields
        assert "period" in data
        assert "hourly_distribution" in data
        assert "daily_distribution" in data
        assert "peak_hour" in data
        assert "peak_day" in data

        # Check hourly_distribution (0-23)
        hourly = data["hourly_distribution"]
        assert isinstance(hourly, dict)
        assert len(hourly) == 24  # 24 hours

        # Check daily_distribution (Monday-Sunday)
        daily = data["daily_distribution"]
        assert isinstance(daily, dict)
        assert "Monday" in daily
        assert "Sunday" in daily

        # Check peak values
        assert isinstance(data["peak_hour"], str)
        assert isinstance(data["peak_day"], str)

    def test_get_usage_patterns_custom_days(self):
        response = self.get("/user/usage/patterns?days=7")

        assert response.status_code == 200
        data = response.json()
        assert data["period"]["days"] == 7

    def test_get_usage_patterns_unauthorized(self):
        client_no_auth = TestClient(self.client.app)
        response = client_no_auth.get("/user/usage/patterns")
        assert response.status_code in [401, 403]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
