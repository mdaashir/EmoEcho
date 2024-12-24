from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SadnessScoreTests(APITestCase):
    def test_single_sadness_score_success(self):
        """
        Test if sadness score is correctly computed for a single text.
        """
        url = reverse("get-sadness-score")
        data = {"text": "This is a very sad day."}
        response = self.client.post(url, data, format="json")

        # Check HTTP response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for the presence of 'score' and 'message' fields in the response
        self.assertIn("score", response.data)
        self.assertIn("message", response.data)

        # Validate sadness thresholds for the score
        score = response.data["score"]
        message = response.data["message"]

        if score < -0.6:
            self.assertEqual(message, "Alarming!")
        elif score < -0.5:
            self.assertEqual(message, "Level 3 : Consultation Needed")
        elif score < -0.4:
            self.assertEqual(message, "Level 2 : Some Help would be preferred")
        elif score < -0.3:
            self.assertEqual(message, "Basic sadness")
        else:
            self.assertEqual(message, "You're Okay!")

    def test_single_sadness_score_missing_text(self):
        """
        Test if API handles missing 'text' field properly.
        """
        url = reverse("get-sadness-score")
        # Missing 'text', providing incorrect field
        data = {"wrong_field": "No text provided."}
        response = self.client.post(url, data, format="json")

        # Check for 400 error and error message in the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "The 'text' field is required.")

    def test_bulk_sadness_score_success(self):
        """
        Test if sadness scores are correctly computed for multiple texts.
        """
        url = reverse("get-bulk-sadness-score")  # Bulk API endpoint
        data = {
            "posts": [
                {"caption": "This is a sad post."},
                {"caption": "What a happy day!"},
                {"caption": ""},
            ]
        }
        response = self.client.post(url, data, format="json")

        # Check HTTP response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("posts", response.data)

        # Assert the number of results matches the input length
        posts_result = response.data["posts"]
        self.assertEqual(len(posts_result), 3)

        # Verify fields for each post
        for post in posts_result:
            self.assertIn("caption", post)
            self.assertIn("score", post)
            self.assertIn("message", post)

    def test_bulk_sadness_score_invalid_posts(self):
        """
        Test if bulk API handles invalid input properly.
        """
        url = reverse("get-bulk-sadness-score")
        # Providing incorrect field instead of "posts"
        data = {"invalid_field": "Invalid input"}
        response = self.client.post(url, data, format="json")

        # Check for 400 error and error message in the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "'posts' field must be a non-empty list."
        )
