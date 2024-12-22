from rest_framework.routers import DefaultRouter
from .views import InstagramAPI

router = DefaultRouter()
# router.register("get-authorization-code",InstagramAPI.get_authorization_code, basename="getAuthorizationCode")
# router.register("get-access-token", InstagramAPI.get_access_token, basename="getAccessToken")
# router.register("get-user-details", InstagramAPI.get_user_details, basename="getDetails")
# router.register("get-user-posts", InstagramAPI.get_user_posts, basename="getUserPosts")
router.register(prefix='', viewset=InstagramAPI, basename="instagram")

urlpatterns = router.urls
