from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class InstagramAPITests(APITestCase):
    def test_get_authorization_code_success(self):
        """
        Test if the API correctly generates the Instagram authorization URL.
        """
        url = reverse("get-authorization-code")
        data = {
            "client_id": "test_client_id",
            "redirect_uri": "https://example.com/redirect",
            "scope": "user_profile,user_media",
            "response_type": "code",
        }
        response = self.client.post(url, data, format="json")

        # Check HTTP response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate the returned authorization URL
        self.assertIn("authorization_url", response.data)
        self.assertIn(data["client_id"], response.data["authorization_url"])
        self.assertIn(data["redirect_uri"], response.data["authorization_url"])

    def test_get_authorization_code_missing_required_fields(self):
        """
        Test if the API handles missing 'client_id' or 'redirect_uri' properly.
        """
        url = reverse("get-authorization-code")
        data = {
            # Missing 'client_id' and 'redirect_uri'
            "scope": "user_profile,user_media",
            "response_type": "code",
        }
        response = self.client.post(url, data, format="json")

        # Check for 400 error and error message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"],
            "'client_id' and 'redirect_uri' fields are required.",
        )

    def test_get_access_token_success(self):
        """
        Test if the API exchanges authorization code for access tokens successfully.
        """
        url = reverse("get-access-token")
        data = {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "redirect_uri": "https://example.com/redirect",
            "code": "test_authorization_code",
        }
        response = self.client.post(url, data, format="json")

        # Check for successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure response includes the token fields
        self.assertIn("access_token", response.data)
        self.assertIn("user_id", response.data)
        self.assertIn("expires_in", response.data)

    def test_get_access_token_missing_fields(self):
        """
        Test if the API handles missing required fields for access token generation.
        """
        url = reverse("get-access-token")
        # Missing 'code' and other required fields
        data = {
            "client_id": "test_client_id",
            "redirect_uri": "https://example.com/redirect",
        }
        response = self.client.post(url, data, format="json")

        # Check for 400 error and descriptive error message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"],
            "All fields ('client_id', 'client_secret', 'redirect_uri', 'code') are required.",
        )

    def test_get_user_details_success(self):
        """
        Test if the API fetches user details successfully given valid credentials.
        """
        url = reverse("get-user-details")
        data = {
            "user_id": "123456789",
            "access_token": "test_access_token",
        }
        response = self.client.post(url, data, format="json")

        # Check for successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user_details", response.data)

    def test_get_user_details_missing_fields(self):
        """
        Test if the API handles missing user_id or access_token properly.
        """
        url = reverse("get-user-details")
        data = {
            # Missing 'user_id'
            "access_token": "test_access_token",
        }
        response = self.client.post(url, data, format="json")

        # Check for 400 error and descriptive error message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "'user_id' and 'access_token' fields are required."
        )

    def test_get_user_posts_success(self):
        """
        Test if the API successfully fetches user posts.
        """
        url = reverse("get-user-posts")
        data = {
            "user_id": "123456789",
            "access_token": "test_access_token",
        }
        response = self.client.post(url, data, format="json")

        # Check for successful response and presence of posts
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("posts", response.data)
        self.assertIsInstance(response.data["posts"], dict)  # Data structure validation

    def test_get_user_posts_missing_fields(self):
        """
        Test if the API handles missing user_id or access_token for fetching posts.
        """
        url = reverse("get-user-posts")
        data = {
            "access_token": "test_access_token",
            # Missing 'user_id'
        }
        response = self.client.post(url, data, format="json")

        # Check for 400 error and descriptive error message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "'user_id' and 'access_token' fields are required."
        )
