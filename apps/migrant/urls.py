from rest_framework.routers import DefaultRouter
from apps.migrant.views import MigrantViewSet


router = DefaultRouter()
router.register(r'migrants', MigrantViewSet)

urlpatterns = router.urls
