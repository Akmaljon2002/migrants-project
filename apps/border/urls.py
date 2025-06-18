from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.border.views import BorderCrossViewSet

router = DefaultRouter()
router.register(r'border-crosses', BorderCrossViewSet)

urlpatterns = [
    path('', include(router.urls)),
]