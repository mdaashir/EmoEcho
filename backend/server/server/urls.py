from django.urls import path, include
from . import swagger

urlpatterns = [
    # Instagram API routes
    path('api/v1/instagram/', include('instagramAPI.urls')),

    # Emotion Analyzer API routes
    path('api/v1/model/', include('emotionAnalyzer.urls')),

    # API Documentation routes
    path('api/v1/docs/', include(swagger.urls)),
]
