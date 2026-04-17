"""Tests for GET /activities endpoint."""
import pytest


class TestActivitiesEndpoint:
    """Test suite for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all 9 activities with 200 status.
        
        Arrange: Client is ready
        Act: Send GET request to /activities
        Assert: Response status is 200 and all 9 activities are returned
        """
        # Arrange
        expected_activity_count = 9

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count
        assert isinstance(activities, dict)

    def test_get_activities_returns_correct_fields(self, client):
        """Test that each activity has required fields.
        
        Arrange: Client is ready
        Act: Send GET request to /activities
        Assert: Each activity contains description, schedule, max_participants, and participants fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_details in activities.items():
            for field in required_fields:
                assert field in activity_details, f"Activity '{activity_name}' missing field: {field}"

    def test_get_activities_response_structure(self, client):
        """Test that response is a dictionary with activity names as keys.
        
        Arrange: Client is ready
        Act: Send GET request to /activities
        Assert: Response is a dict where keys are activity names and values are activity details
        """
        # Arrange
        # (no setup needed)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        assert isinstance(activities, dict)
        # Verify all keys are strings (activity names)
        for activity_name in activities.keys():
            assert isinstance(activity_name, str)
            assert len(activity_name) > 0

    def test_get_activities_participants_is_list(self, client):
        """Test that participants field is a list in each activity.
        
        Arrange: Client is ready
        Act: Send GET request to /activities
        Assert: participants field contains a list (possibly empty)
        """
        # Arrange
        # (no setup needed)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_details in activities.items():
            assert isinstance(
                activity_details["participants"], list
            ), f"Activity '{activity_name}' participants should be a list"

    def test_get_activities_max_participants_is_number(self, client):
        """Test that max_participants field is a number in each activity.
        
        Arrange: Client is ready
        Act: Send GET request to /activities
        Assert: max_participants field contains a positive integer
        """
        # Arrange
        # (no setup needed)

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_details in activities.items():
            assert isinstance(
                activity_details["max_participants"], int
            ), f"Activity '{activity_name}' max_participants should be an integer"
            assert (
                activity_details["max_participants"] > 0
            ), f"Activity '{activity_name}' max_participants should be positive"
