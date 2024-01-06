from django.urls import path
from . import views

urlpatterns = [
    path('get-authorization-code/', views.getAuthorizationCode, name='getAuthorizationCode'),
    path('get-access-token/', views.getAcessToken, name='getAcessToken'),
    path('get-user-details/', views.getUserDetails, name='getDetails'),
    path('get-user-posts/', views.getUserPosts, name='getUserPosts'),
]