"""
Mock objects for testing without real Supabase connection
"""

from unittest.mock import MagicMock
from uuid import uuid4


class MockSupabaseResponse:
    """Mock Supabase response object"""

    def __init__(self, data=None, count=None):
        self.data = data if data is not None else []
        self.count = count if count is not None else (len(self.data) if isinstance(self.data, list) else 1)


class MockSupabaseTable:
    """Mock Supabase table interface"""

    def __init__(self, table_name: str, storage: dict = None):
        self.table_name = table_name
        self.storage = storage if storage is not None else {}
        self._query_filters = []
        self._select_fields = "*"

    def select(self, fields="*"):
        """Mock select method"""
        self._select_fields = fields
        return self

    def insert(self, data):
        """Mock insert method"""
        # Ensure data has an ID
        if isinstance(data, dict):
            if "id" not in data:
                data["id"] = str(uuid4())
            table_data = self.storage.setdefault(self.table_name, [])
            table_data.append(data)
        elif isinstance(data, list):
            for item in data:
                if "id" not in item:
                    item["id"] = str(uuid4())
            self.storage.setdefault(self.table_name, []).extend(data)
        return self

    def update(self, data):
        """Mock update method"""
        # Apply update to filtered records
        table_data = self.storage.get(self.table_name, [])
        for item in table_data:
            if self._matches_filters(item):
                item.update(data)
        return self

    def delete(self):
        """Mock delete method"""
        table_data = self.storage.get(self.table_name, [])
        self.storage[self.table_name] = [item for item in table_data if not self._matches_filters(item)]
        return self

    def eq(self, column, value):
        """Mock eq filter"""
        self._query_filters.append(("eq", column, value))
        return self

    def neq(self, column, value):
        """Mock neq filter"""
        self._query_filters.append(("neq", column, value))
        return self

    def like(self, column, pattern):
        """Mock like filter"""
        self._query_filters.append(("like", column, pattern))
        return self

    def execute(self):
        """Execute the query and return mock response"""
        table_data = self.storage.get(self.table_name, [])

        # Apply filters
        filtered_data = [item for item in table_data if self._matches_filters(item)]

        # Reset filters for next query
        self._query_filters = []
        self._select_fields = "*"

        return MockSupabaseResponse(data=filtered_data)

    def _matches_filters(self, item):
        """Check if item matches all current filters"""
        if not self._query_filters:
            return True

        for filter_type, column, value in self._query_filters:
            if filter_type == "eq":
                if item.get(column) != value:
                    return False
            elif filter_type == "neq":
                if item.get(column) == value:
                    return False
            elif filter_type == "like":
                # Simple pattern matching (% as wildcard)
                pattern = value.replace("%", ".*")
                import re

                if not re.match(pattern, str(item.get(column, ""))):
                    return False

        return True


class MockSupabaseAuth:
    """Mock Supabase auth interface"""

    def __init__(self):
        self.admin = MockSupabaseAuthAdmin()

    def sign_in_with_password(self, credentials):
        """Mock sign in"""
        # Return a mock session with a fake token
        user_id = str(uuid4())
        access_token = f"mock_token_{user_id}"

        session = MagicMock()
        session.access_token = access_token
        session.refresh_token = "mock_refresh_token"

        user = MagicMock()
        user.id = user_id
        user.email = credentials.get("email")

        response = MagicMock()
        response.session = session
        response.user = user

        return response

    def sign_up(self, credentials):
        """Mock sign up"""
        return self.sign_in_with_password(credentials)


class MockSupabaseAuthAdmin:
    """Mock Supabase auth admin interface"""

    def delete_user(self, user_id):
        """Mock delete user"""
        return {"id": user_id}


class MockSupabaseClient:
    """Mock Supabase client"""

    def __init__(self, shared_storage=None):
        self.storage = shared_storage if shared_storage is not None else {}
        self.auth = MockSupabaseAuth()

    def table(self, table_name: str):
        """Return a mock table"""
        return MockSupabaseTable(table_name, self.storage)

    def from_(self, table_name: str):
        """Alias for table()"""
        return self.table(table_name)
