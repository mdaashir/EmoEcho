from django.urls import path, include

urlpatterns = [
    path('instagram-api/', include('instagramAPI.urls')),
    path('emotion-analyzer/', include('emotionAnalyzer.urls'))
]
