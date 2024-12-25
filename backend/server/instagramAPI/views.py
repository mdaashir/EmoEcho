from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from .schemas import (
    authorization_code_request_body,
    authorization_code_response,
    access_token_request_body,
    access_token_response,
    user_details_request_body,
    user_details_response,
    user_posts_request_body,
    user_posts_response,
)
import requests

class GetAuthorizationCodeView(APIView):
    """
    API to generate Instagram Authorization URL.
    """

    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=authorization_code_request_body,
        responses=authorization_code_response,
        operation_description="Generates an Instagram Authorization URL based on the provided parameters.",
    )
    def post(self, request):
        client_id = request.data.get("client_id")
        redirect_uri = request.data.get("redirect_uri")
        scope = request.data.get("scope")
        response_type = request.data.get("response_type")

        if not client_id or not redirect_uri:
            return Response(
                {"error": "'client_id' and 'redirect_uri' fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        url = f"https://api.instagram.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type={response_type}"

        return Response(
            {"authorization_url": url},
            status=status.HTTP_200_OK,
        )


class GetAccessTokenView(APIView):
    """
    API to exchange an Instagram authorization code for an access token.
    """

    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=access_token_request_body,
        responses=access_token_response,
        operation_description="Exchanges an authorization code for a short-lived access token.",
    )
    def post(self, request):
        client_id = request.data.get("client_id")
        client_secret = request.data.get("client_secret")
        redirect_uri = request.data.get("redirect_uri")
        code = request.data.get("code")

        if not all([client_id, client_secret, redirect_uri, code]):
            return Response(
                {
                    "error": "All fields ('client_id', 'client_secret', 'redirect_uri', 'code') are required."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        url = "https://api.instagram.com/oauth/access_token"
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code,
        }

        try:
            response = requests.post(url, data=payload)

            # Further process to get long-lived access token
            if response.status_code == 200:
                response_data = response.json()
                short_lived_token = response_data.get("access_token")
                user_id = response_data.get("user_id")

                long_lived_response = self.get_long_lived_access_token(
                    short_lived_token, client_secret, user_id
                )
                return long_lived_response
            else:
                return Response(
                    {
                        "error": f"Failed to exchange code for access token. Status code: {response.status_code}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception:
            return Response(
                {"error": "An error occurred while exchanging the authorization code."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def get_long_lived_access_token(short_lived_token, client_secret, user_id):
        """
        Internal method to exchange short-lived token for a long-lived token.
        """
        url = f"https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret={client_secret}&access_token={short_lived_token}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                response_data = response.json()
                return Response(
                    {
                        "access_token": response_data.get("access_token"),
                        "user_id": user_id,
                        "expires_in": response_data.get("expires_in"),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "error": f"Failed to retrieve long-lived token. Status code: {response.status_code}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception:
            return Response(
                {
                    "error": "An error occurred while retrieving the long-lived access token."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetUserDetailsView(APIView):
    """
    API to fetch Instagram user details using the user ID and access token.
    """

    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=user_details_request_body,
        responses=user_details_response,
        operation_description="Fetches user details from the Instagram Graph API.",
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        access_token = request.data.get("access_token")

        if not user_id or not access_token:
            return Response(
                {"error": "'user_id' and 'access_token' fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        url = f"https://graph.instagram.com/{user_id}?fields=id,username&access_token={access_token}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                response_data = response.json()
                return Response(
                    {"user_details": response_data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "error": f"Failed to fetch user details. Status code: {response.status_code}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception:
            return Response(
                {"error": "An error occurred while fetching user details."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetUserPostsView(APIView):
    """
    API to fetch Instagram user posts using the user ID and access token.
    """

    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=user_posts_request_body,
        responses=user_posts_response,
        operation_description="Fetches user posts from the Instagram Graph API.",
    )
    def post(self, request):
        user_id = request.data.get("user_id")
        access_token = request.data.get("access_token")

        if not user_id or not access_token:
            return Response(
                {"error": "'user_id' and 'access_token' fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        url = f"https://graph.instagram.com/{user_id}/media?fields=id,username,caption,media_type,media_url&access_token={access_token}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                response_data = response.json()
                return Response(
                    {"posts": response_data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "error": f"Failed to fetch user posts. Status code: {response.status_code}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception:
            return Response(
                {"error": "An error occurred while fetching user posts."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
