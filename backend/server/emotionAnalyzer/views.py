from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from .schemas import (
    get_sadness_score_request_body,
    get_sadness_score_responses,
    get_bulk_sadness_score_request_body,
    get_bulk_sadness_score_responses,
)
from .utils import (preprocessText, sentimentAnalysis)

class GetSadnessScoreView(APIView):
    """
    API to compute sadness score for a single text input.
    """

    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=get_sadness_score_request_body,  # Swagger schema for request body
        responses=get_sadness_score_responses,  # Swagger schema for responses
        operation_description="Computes the sadness score for a text input.",
    )
    def post(self, request):
        text = request.data.get("text", "")  # Retrieve the text from the request

        if not text:  # Validate input
            return Response(
                {"error": "The 'text' field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            cleaned_text = preprocessText(text)
            sadness_score, message = sentimentAnalysis(cleaned_text)

            return Response(
                {"score": sadness_score, "message": message},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": "An error occurred while computing sadness score."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetBulkSadnessScoreView(APIView):
    """
    API to compute sadness scores for multiple text inputs (bulk operation).
    """

    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=get_bulk_sadness_score_request_body,  # Swagger schema for input
        responses=get_bulk_sadness_score_responses,  # Swagger schema for responses
        operation_description="Computes sadness scores for multiple text inputs provided in bulk.",
    )
    def post(self, request):
        posts = request.data.get("posts", [])  # Retrieve posts from the request

        if not posts or not isinstance(posts, list):  # Validate input
            return Response(
                {"error": "'posts' field must be a non-empty list."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = []
            for post in posts:
                caption = post.get("caption", "")
                if caption:  # Validate caption in individual items
                    cleaned_text = preprocessText(post['caption'])
                    sadness_score, message = sentimentAnalysis(cleaned_text)
                    result.append(
                        {"caption": caption, "score": sadness_score, "message": message}
                    )
                else:
                    result.append({"caption": "No Caption Available", "score": 0, "message": "No Details Available"})

            return Response({"posts": result}, status=status.HTTP_200_OK)

        except Exception as e:  # Handle unexpected errors
            return Response(
                {"error": "An error occurred while processing bulk sadness scores."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
