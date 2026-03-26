"""
02_user_registration.py

Second test in the sequential stack test suite.
Verifies user registration and retrieval flows.

Demonstrates:
- Full-loop assertion layering (primary, second-order, third-order)
- User journey testing
- Database state verification via API
- Sequential dependency on startup tests
"""

import pytest
from httpx import Response


@pytest.fixture
def created_user_id(http_client, wait_for_ready) -> str:
    """
    Create a user and return the ID.
    Shared across tests to demonstrate sequential flow.
    """
    wait_for_ready()

    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "SecurePass123!",
    }

    response = http_client.post("/users", json=user_data)

    # Strict assertion — no conditional checks
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"

    data = response.json()
    assert "id" in data
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "password" not in data  # Password never returned

    return data["id"]


@pytest.mark.stack
class TestUserRegistration:
    """Verify user registration and management flows."""

    def test_create_user_returns_201(self, http_client, wait_for_ready):
        """Primary assertion: POST /users creates a new user."""
        wait_for_ready()

        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "SecurePass123!",
        }

        response = http_client.post("/users", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["id"]
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert data["created_at"]

    def test_get_user_by_id(self, http_client, created_user_id):
        """
        Primary and second-order assertion: retrieve created user.
        Depends on user being created (demonstrates sequential design).
        """
        # created_user_id fixture ensures a user exists
        assert created_user_id  # Verify fixture ran

        response = http_client.get(f"/users/{created_user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_user_id
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"

    def test_user_list_includes_created_user(self, http_client, created_user_id):
        """Second-order assertion: verify user appears in list endpoint."""
        response = http_client.get("/users")

        assert response.status_code == 200
        data = response.json()
        assert "users" in data

        user_ids = [u["id"] for u in data["users"]]
        assert created_user_id in user_ids

        # Find and verify the full user object
        created_user = next((u for u in data["users"] if u["id"] == created_user_id), None)
        assert created_user is not None
        assert created_user["username"] == "testuser"

    def test_duplicate_email_returns_409(self, http_client, created_user_id):
        """Verify uniqueness constraint is enforced."""
        duplicate_data = {
            "email": "test@example.com",  # Same email
            "username": "different",
            "password": "AnotherPass123!",
        }

        response = http_client.post("/users", json=duplicate_data)

        assert response.status_code == 409
        data = response.json()
        assert "error" in data
        assert "already exists" in data["error"].lower()

    def test_user_is_audited_in_logs(self, http_client, created_user_id):
        """Third-order assertion: verify audit log via admin API."""
        response = http_client.get("/admin/audit/users")

        assert response.status_code == 200
        data = response.json()
        assert "entries" in data

        # Find the creation event for our user
        creation_events = [
            e for e in data["entries"]
            if e.get("action") == "USER_CREATED"
            and e.get("entity_id") == created_user_id
        ]

        assert len(creation_events) > 0, "User creation event not found in audit log"

        event = creation_events[0]
        assert event["entity_type"] == "user"
        assert "timestamp" in event

    def test_user_data_persists(self, http_client, created_user_id):
        """
        Verify data persistence across requests.
        This tests that volumes work correctly.
        """
        # First read
        response1 = http_client.get(f"/users/{created_user_id}")
        assert response1.status_code == 200
        original_data = response1.json()

        # Second read (should be identical)
        response2 = http_client.get(f"/users/{created_user_id}")
        assert response2.status_code == 200
        assert response2.json() == original_data

    def test_invalid_user_id_returns_404(self, http_client):
        """Verify proper error handling for non-existent users."""
        response = http_client.get("/users/nonexistent-id")

        assert response.status_code == 404
        data = response.json()
        assert "error" in data

    def test_update_user_email(self, http_client, created_user_id):
        """Verify user can be updated."""
        new_email = "updated@example.com"

        response = http_client.patch(
            f"/users/{created_user_id}",
            json={"email": new_email}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == new_email

        # Verify the change persisted
        get_response = http_client.get(f"/users/{created_user_id}")
        assert get_response.json()["email"] == new_email
