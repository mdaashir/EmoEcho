from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("get-authorization-code",views.getAuthorizationCode, basename="getAuthorizationCode")
router.register("get-access-token", views.getAccessToken, basename="getAcessToken")
router.register("get-user-details", views.getUserDetails, basename="getDetails")
router.register("get-user-posts", views.getUserPosts, basename="getUserPosts")

urlpatterns = [path("instagram/", include(router.urls))]
