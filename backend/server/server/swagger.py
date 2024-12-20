# from django.urls import path
# from rest_framework.permissions import AllowAny
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="EmoEcho API Documentation",
#         default_version="v1",
#         description="This is the API documentation for the EmoEcho project. EmoEcho is a platform designed to analyze and interpret emotional responses from textual data. The API provides endpoints for submitting text for analysis, retrieving emotional insights, and managing user data. This documentation provides detailed information about each endpoint, including request and response formats, authentication methods, and error handling.",
#         contact=openapi.Contact(email="s.mohamedaashir@gmail.com"),
#         license=openapi.License(name="MIT License"),
#     ),
#     public=False,
#     permission_classes=(AllowAny,),
#     validators=["ssv"],
# )

# urls = [
#     # Endpoint for Swagger UI
#     path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),

#     # Endpoint for ReDoc UI
#     path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),
# ]
