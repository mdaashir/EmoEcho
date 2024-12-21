from rest_framework.routers import DefaultRouter
from .views import getAuthorizationCode, getAccessToken, getUserPosts, getUserDetails

router = DefaultRouter()
router.register("get-authorization-code",getAuthorizationCode, basename="getAuthorizationCode")
router.register("get-access-token", getAccessToken, basename="getAccessToken")
router.register("get-user-details", getUserDetails, basename="getDetails")
router.register("get-user-posts", getUserPosts, basename="getUserPosts")

urlpatterns = router.urls
