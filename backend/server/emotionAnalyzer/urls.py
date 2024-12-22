from rest_framework.routers import DefaultRouter
from .views import EmotionAnalyzer

router = DefaultRouter()
# router.register("get-sadness-score", EmotionAnalyzer.get_sadness_score, basename='getSadnessScore')
# router.register("get-bulk-sadness-score", EmotionAnalyzer.get_bulk_sadness_score, basename='getBulkSadnessScore')
router.register(prefix='', viewset=EmotionAnalyzer, basename='model')

urlpatterns = router.urls
