from drf_yasg import openapi

# --- Authorization Code ---
authorization_code_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["client_id", "redirect_uri", "scope", "response_type"],
    properties={
        "client_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="Instagram App Client ID."
        ),
        "redirect_uri": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Callback URL where the authorization code will be sent.",
        ),
        "scope": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Permissions requested by the app (e.g., user_profile, user_media).",
        ),
        "response_type": openapi.Schema(
            type=openapi.TYPE_STRING, description="Expected response type, e.g., code."
        ),
    },
    example={
        "client_id": "your_client_id",
        "redirect_uri": "https://myapp.com/auth_callback",
        "scope": "user_profile,user_media",
        "response_type": "code",
    },
)

authorization_code_response = {
    200: openapi.Response(
        description="The Instagram authorization URL to acquire the authorization code.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "authorization_url": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Authorization URL to get the authorization code.",
                )
            },
        ),
        examples={"application/json": {"authorization_url": "url_to_get_authorization_code"}},
    ),
    400: openapi.Response(
        description="Invalid input. For example, missing 'client_id' and 'redirect_uri' field.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(
                    type=openapi.TYPE_STRING,  # Error messages are strings
                    description="Details about the error.",
                )
            },
            example={"error": "'client_id' and 'redirect_uri' fields are required."},
        ),
    ),
}

# --- Access Token ---
access_token_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["client_id", "client_secret", "redirect_uri", "code"],
    properties={
        "client_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="Your Instagram app's Client ID."
        ),
        "client_secret": openapi.Schema(
            type=openapi.TYPE_STRING, description="Your Instagram app's Client Secret."
        ),
        "redirect_uri": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Callback URL matching the one specified in Instagram App settings.",
        ),
        "code": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="The authorization code received after user login.",
        ),
    },
    example={
        "client_id": "your_client_id",
        "client_secret": "your_client_secret",
        "redirect_uri": "https://yourapp.com/auth_callback",
        "code": "authorization_code",
    },
)

access_token_response = {
    200: openapi.Response(
        description="Access token and user ID received.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "access_token": openapi.Schema(type=openapi.TYPE_STRING),
                "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "expires_in": openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        ),
        examples={
            "application/json": {
                "access_token": "long_lived_access_token",
                "user_id": 123456789,
                "expires_in": 5184000,
            }
        },
    ),
    400: openapi.Response(
        description="Error decoding JSON data.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(
                    type=openapi.TYPE_STRING,  # Error messages are strings
                    description="Details about the error.",
                )
            },
        ),
        examples={
            "application/json": {
                "error": "All fields ('client_id', 'client_secret', 'redirect_uri', 'code') are required."
            }
        },
    ),
    500: openapi.Response(
        description="Error occurred while fetching the access token.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(
                    type=openapi.TYPE_STRING,  # Error messages are strings
                    description="Details about the error.",
                )
            },
        ),
        examples={
            "application/json": {
                "error": "An error occurred while exchanging the authorization code."
            }
        },
    ),
}

# --- User Details ---
user_details_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["user_id", "access_token"],
    properties={
        "user_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="User's Instagram ID."
        ),
        "access_token": openapi.Schema(
            type=openapi.TYPE_STRING, description="Instagram API Access Token."
        ),
    },
    example={"user_id": "123456789", "access_token": "valid_access_token"},
)

user_details_response = {
    200: openapi.Response(
        description="User details including ID and username.",
        examples={
            "application/json": {
                "response": {"id": "123456789", "username": "instagram_username"}
            }
        },
    ),
    400: openapi.Response(
        description="Error decoding JSON data.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(
                    type=openapi.TYPE_STRING,  # Error messages are strings
                    description="Details about the error.",
                )
            },
        ),
        examples={
            "application/json": {"error": "Error decoding JSON data: <error_message>"},
            "application/json": {
                "error": "'user_id' and 'access_token' fields are required."
            },
        },
    ),
    500: openapi.Response(
        description="Error occurred while fetching user details.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(
                    type=openapi.TYPE_STRING,  # Error messages are strings
                    description="Details about the error.",
                )
            },
        ),
        examples={
            "application/json": {
                "error": "An error occurred while fetching user details."
            }
        },
    ),
}

# --- User Posts ---
user_posts_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["user_id", "access_token"],
    properties={
        "user_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="User's Instagram ID."
        ),
        "access_token": openapi.Schema(
            type=openapi.TYPE_STRING, description="Instagram API Access Token."
        ),
    },
    example={"user_id": "123456789", "access_token": "valid_access_token"},
)

user_posts_response = {
    200: openapi.Response(
        description="User's posts including media details.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "data": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(type=openapi.TYPE_STRING),
                            "media_type": openapi.Schema(type=openapi.TYPE_STRING),
                            "media_url": openapi.Schema(type=openapi.TYPE_STRING),
                            "username": openapi.Schema(type=openapi.TYPE_STRING),
                            "caption": openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                )
            },
        ),
        examples={
            "application/json": {
                "response": {
                    "data": [
                        {
                            "id": "17895695668004550",
                            "media_type": "IMAGE",
                            "media_url": "https://example.com/media.jpg",
                            "username": "instagram_username",
                            "caption": "Sample caption",
                        }
                    ]
                }
            }
        },
    ),
    400: openapi.Response(
        description="Error decoding JSON data.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(
                    type=openapi.TYPE_STRING,  # Error messages are strings
                    description="Details about the error.",
                )
            },
        ),
        examples={
            "application/json": {"error": "Error decoding JSON data"},
            "application/json": {
                "error": "'user_id' and 'access_token' fields are required."
            },
        },
    ),
    500: openapi.Response(
        description="Error retrieving user posts.",
        examples={
            "application/json": {
                "error": "An error occurred while fetching user posts."
            }
        },
    ),
}
