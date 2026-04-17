"""Tests for POST /activities/{activity_name}/signup endpoint."""
import pytest


class TestSignupEndpoint:
    """Test suite for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_valid_activity_success(self, client):
        """Test successful signup for an existing activity.
        
        Arrange: Valid activity name (Chess Club) and email address
        Act: Send POST request to /activities/Chess Club/signup with email parameter
        Assert: Response status is 200 and success message is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "test@example.com"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity_name in result["message"]

    def test_signup_duplicate_email_returns_400(self, client):
        """Test that duplicate signup for same activity returns 400 error.
        
        Arrange: Email already signed up for an activity
        Act: First signup succeeds, then attempt second signup with same email
        Assert: Second signup returns 400 status and error detail about already signed up
        """
        # Arrange
        activity_name = "Programming Class"
        email = "duplicate@example.com"

        # First signup - should succeed
        client.post(f"/activities/{activity_name}/signup?email={email}")

        # Act - attempt duplicate signup
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "already signed up" in result["detail"].lower()

    def test_signup_nonexistent_activity_returns_404(self, client):
        """Test that signup for non-existent activity returns 404 error.
        
        Arrange: Activity name that doesn't exist
        Act: Send POST request to /activities/NonExistentActivity/signup
        Assert: Response status is 404 and error detail about activity not found
        """
        # Arrange
        activity_name = "NonExistentActivity"
        email = "test@example.com"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "not found" in result["detail"].lower()

    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup adds participant to activity's participant list.
        
        Arrange: Get initial participant list for an activity
        Act: Sign up a new participant, then fetch activities again
        Assert: New participant email appears in the activity's participant list
        """
        # Arrange
        activity_name = "Gym Class"
        email = "newsignup@example.com"

        # Get initial activities
        initial_response = client.get("/activities")
        initial_activities = initial_response.json()
        initial_participants = initial_activities[activity_name]["participants"].copy()

        # Act - signup
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup_response.status_code == 200

        # Get updated activities
        updated_response = client.get("/activities")
        updated_activities = updated_response.json()
        updated_participants = updated_activities[activity_name]["participants"]

        # Assert
        assert email in updated_participants
        assert len(updated_participants) == len(initial_participants) + 1

    def test_signup_with_multiple_activities(self, client):
        """Test that same email can sign up for multiple activities.
        
        Arrange: Same email, two different activities
        Act: Send POST for first activity, then POST for second activity
        Assert: Both signups succeed with 200 status
        """
        # Arrange
        email = "multi@example.com"
        activity1 = "Basketball Team"
        activity2 = "Tennis Club"

        # Act - signup for first activity
        response1 = client.post(f"/activities/{activity1}/signup?email={email}")

        # Act - signup for second activity
        response2 = client.post(f"/activities/{activity2}/signup?email={email}")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify both activities show the participant
        activities = client.get("/activities").json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]

    def test_signup_return_message_format(self, client):
        """Test that signup success message has correct format.
        
        Arrange: Valid activity and unique email
        Act: Send POST request to /activities/{activity}/signup
        Assert: Return message contains both email and activity name
        """
        # Arrange
        activity_name = "Art Studio"
        email = "format@example.com"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        result = response.json()
        message = result["message"]
        assert "Signed up" in message or "signup" in message.lower()
        assert email in message
        assert activity_name in message
