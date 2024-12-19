from django.urls import path
from . import views

urlpatterns = [
    path('get-sadness-score/', views.getSadnessScore, name='getSadnessScore'),
    path('get-bulk-sadness-score/', views.getBulkSadnessScore, name='getBulkSadnessScore'),
]
