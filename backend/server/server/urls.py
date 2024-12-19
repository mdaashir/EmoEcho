from django.urls import path, include

urlpatterns = [
    path('api/v1/instagram/', include('instagramAPI.urls')),
    path('api/v1/model/', include('emotionAnalyzer.urls'))
]
