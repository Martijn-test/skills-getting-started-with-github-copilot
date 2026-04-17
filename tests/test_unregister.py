"""Tests for DELETE /activities/{activity_name}/unregister endpoint."""
import pytest


class TestUnregisterEndpoint:
    """Test suite for the DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_valid_participant_success(self, client):
        """Test successful unregistration of a participant.
        
        Arrange: Sign up a participant first, then prepare to unregister
        Act: Send DELETE request to /activities/{activity}/unregister with email
        Assert: Response status is 200 and success message is returned
        """
        # Arrange
        activity_name = "Chess Club"
        email = "unregister_test@example.com"
        
        # First, sign up
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup_response.status_code == 200

        # Act - unregister
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity_name in result["message"]

    def test_unregister_removes_participant_from_activity(self, client):
        """Test that unregister removes participant from activity's participant list.
        
        Arrange: Sign up a participant
        Act: Unregister the participant, then fetch activities
        Assert: Participant email no longer appears in activity's participant list
        """
        # Arrange
        activity_name = "Programming Class"
        email = "remove_test@example.com"
        
        # Sign up first
        client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Verify participant was added
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]

        # Act - unregister
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response.status_code == 200

        # Assert
        updated_activities = client.get("/activities").json()
        assert email not in updated_activities[activity_name]["participants"]

    def test_unregister_not_signed_up_returns_400(self, client):
        """Test that unregistering someone not signed up returns 400 error.
        
        Arrange: Email that is not signed up for the activity
        Act: Send DELETE request to unregister
        Assert: Response status is 400 and error detail about not being signed up
        """
        # Arrange
        activity_name = "Gym Class"
        email = "not_signed_up@example.com"

        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "not signed up" in result["detail"].lower()

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Test that unregistering from non-existent activity returns 404 error.
        
        Arrange: Activity name that doesn't exist
        Act: Send DELETE request to /activities/NonExistentActivity/unregister
        Assert: Response status is 404 and error detail about activity not found
        """
        # Arrange
        activity_name = "NonExistentActivity"
        email = "test@example.com"

        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "not found" in result["detail"].lower()

    def test_unregister_then_signup_again(self, client):
        """Test that participant can sign up again after unregistering.
        
        Arrange: Sign up a participant
        Act: Unregister, then sign up again
        Assert: Both operations succeed and participant is in list at the end
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "signup_again@example.com"

        # First signup
        response1 = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response1.status_code == 200

        # Unregister
        response2 = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response2.status_code == 200

        # Act - signup again
        response3 = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response3.status_code == 200
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]

    def test_unregister_multiple_times_fails_on_second(self, client):
        """Test that unregistering twice fails on the second attempt.
        
        Arrange: Sign up a participant
        Act: Unregister successfully, then attempt to unregister again
        Assert: Second unregister returns 400 error
        """
        # Arrange
        activity_name = "Tennis Club"
        email = "double_unregister@example.com"

        # Sign up
        client.post(f"/activities/{activity_name}/signup?email={email}")

        # First unregister - should succeed
        response1 = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response1.status_code == 200

        # Act - attempt second unregister
        response2 = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        # Assert
        assert response2.status_code == 400
        result = response2.json()
        assert "not signed up" in result["detail"].lower()

    def test_unregister_one_activity_does_not_affect_others(self, client):
        """Test that unregistering from one activity doesn't affect others.
        
        Arrange: Sign up for multiple activities
        Act: Unregister from one activity
        Assert: Participant remains in other activities
        """
        # Arrange
        email = "multiple@example.com"
        activity1 = "Art Studio"
        activity2 = "Music Band"

        # Sign up for both
        client.post(f"/activities/{activity1}/signup?email={email}")
        client.post(f"/activities/{activity2}/signup?email={email}")

        # Act - unregister from first activity only
        response = client.delete(f"/activities/{activity1}/unregister?email={email}")
        assert response.status_code == 200

        # Assert
        activities = client.get("/activities").json()
        assert email not in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]
