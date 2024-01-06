from django.urls import path
from . import views

urlpatterns = [
    path('getSadnessScore/', views.getSadnessScore, name='getSadnessScore'),
    path('getBulkSadnessScore/', views.getBulkSadnessScore, name='getBulkSadnessScore'),
]