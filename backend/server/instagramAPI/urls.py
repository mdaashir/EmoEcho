from django.urls import path
from .views import (
    GetAuthorizationCodeView,
    GetAccessTokenView,
    GetUserDetailsView,
    GetUserPostsView,
)

urlpatterns = [
    path('get-authorization-code/', GetAuthorizationCodeView.as_view(), name='get-authorization-code'),
    path('get-access-token/', GetAccessTokenView.as_view(), name='get-access-token'),
    path('get-user-details/', GetUserDetailsView.as_view(), name='get-user-details'),
    path('get-user-posts/', GetUserPostsView.as_view(), name='get-user-posts'),
]
