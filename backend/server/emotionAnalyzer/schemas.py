from drf_yasg import openapi

# --- get_sadness_score API ---
get_sadness_score_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["text"],  # Ensure this field is mandatory
    properties={
        "text": openapi.Schema(
            type=openapi.TYPE_STRING,  # Input text must be a string
            description="The text content for which sadness score needs to be computed.",
            example="I'm feeling really down today and struggling to concentrate.",
        ),
    },
)

get_sadness_score_responses = {
    200: openapi.Response(
        description="Successfully computed sadness score.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "score": openapi.Schema(
                    type=openapi.TYPE_NUMBER,  # A number (float or int) to represent the sadness score
                    description="The computed sadness score (compound score from sentiment analysis).",
                ),
                "message": openapi.Schema(
                    type=openapi.TYPE_STRING,  # A string message describing the sentiment level
                    description="Message describing the sentiment level, such as alarming or consultation needed.",
                ),
            },
        ),
        examples={"application/json": {"score": -0.65, "message": "Alarming!"}},
    ),
    400: openapi.Response(
        description="Invalid input. For example, missing 'text' field.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(
                    type=openapi.TYPE_STRING,  # Error messages are strings
                    description="Details about the error.",
                )
            },
            example={"error": "The 'text' field is required."},
        ),
    ),
    500: openapi.Response(
        description="Error occurred while computing the sadness score.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(
                    type=openapi.TYPE_STRING,  # Error messages are strings
                    description="Details about the server error.",
                )
            },
            example={"error": "An error occurred while computing Sadness Score."},
        ),
    ),
}

# --- get_bulk_sadness_score API ---
get_bulk_sadness_score_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["posts"],  # Ensure this field is mandatory
    properties={
        "posts": openapi.Schema(
            type=openapi.TYPE_ARRAY,  # Expect an array of posts
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=["caption"],  # Each post object must have a caption
                properties={
                    "caption": openapi.Schema(
                        type=openapi.TYPE_STRING,  # Each caption must be a string
                        description="The caption or text content of a single post.",
                        example="Feeling very sad and lonely.",
                    ),
                },
            ),
            description="List of posts containing captions for bulk sadness score computation.",
        ),
    },
    example={
        "posts": [
            {"caption": "Feeling sad and frustrated."},
            {"caption": "Struggling with work and emotions today."},
        ]
    },
)

get_bulk_sadness_score_responses = {
    200: openapi.Response(
        description="Successfully computed sadness scores for all posts.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "posts": openapi.Schema(
                    type=openapi.TYPE_ARRAY,  # The response is an array of processed posts
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "caption": openapi.Schema(
                                type=openapi.TYPE_STRING,  # Original caption
                                description="The original caption text.",
                            ),
                            "score": openapi.Schema(
                                type=openapi.TYPE_NUMBER,  # The computed sadness score (float or int)
                                description="The computed sadness score for the caption.",
                            ),
                            "message": openapi.Schema(
                                type=openapi.TYPE_STRING,  # The message about sentiment level
                                description="Message describing the sentiment level for the caption.",
                            ),
                        },
                    ),
                ),
            },
        ),
        examples={
            "application/json": {
                "posts": [
                    {
                        "caption": "Feeling sad and frustrated.",
                        "score": -0.6,
                        "message": "Level 3 : Consultation Needed",
                    },
                    {
                        "caption": "Struggling with work and emotions today.",
                        "score": -0.45,
                        "message": "Level 2 : Some Help would be preferred",
                    },
                ]
            }
        },
    ),
    400: openapi.Response(
        description="Invalid input, such as missing 'posts' field or captions.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(
                    type=openapi.TYPE_STRING,  # Error messages are strings
                    description="Details about the error.",
                )
            },
            example={"error": "Field 'posts' is required."},
        ),
    ),
    500: openapi.Response(
        description="Error occurred while computing the sadness scores.",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(
                    type=openapi.TYPE_STRING,  # Error messages are strings
                    description="Details about the server error.",
                )
            },
            example={"error": "An error occurred while computing Sadness Score."},
        ),
    ),
}
