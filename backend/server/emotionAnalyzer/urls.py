from rest_framework.routers import DefaultRouter
from .views import getSadnessScore, getBulkSadnessScore

router = DefaultRouter()
router.register("get-sadness-score", getSadnessScore, basename='getSadnessScore')
router.register("get-bulk-sadness-score", getBulkSadnessScore, basename='getBulkSadnessScore')

urlpatterns = router.urls
