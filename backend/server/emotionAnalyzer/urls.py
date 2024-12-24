from django.urls import path
from .views import GetSadnessScoreView, GetBulkSadnessScoreView

urlpatterns = [
    path('get-sadness-score/', GetSadnessScoreView.as_view(), name='get-sadness-score'),
    path('get-bulk-sadness-score/', GetBulkSadnessScoreView.as_view(), name='get-bulk-sadness-score'),
]
