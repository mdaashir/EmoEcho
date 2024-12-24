from django.views.generic.base import TemplateView
from django.urls import path, include

from . import swagger

urlpatterns = [
    # Welcome page
    path("", TemplateView.as_view(template_name="welcome.html"), name="welcome"),
    # Instagram API routes
    path("api/v1/instagram/", include("instagramAPI.urls")),
    # Emotion Analyzer API routes
    path("api/v1/model/", include("emotionAnalyzer.urls")),
    # API Documentation routes
    path("api/v1/docs/", include(swagger.urls)),
]
