from django.urls import path, include

urlpatterns = [
    path('api/', include('instagramAPI.urls')),
    path('api/', include('emotionAnalyzer.urls'))
]
