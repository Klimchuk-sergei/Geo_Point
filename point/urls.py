from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PointMessageViewSet, PointViewSet

router = DefaultRouter()
router.register(r"points", PointViewSet, basename="point")
router.register(r"points/messages", PointMessageViewSet, basename="pointmessage")

urlpatterns = [
    path("", include(router.urls)),
]
