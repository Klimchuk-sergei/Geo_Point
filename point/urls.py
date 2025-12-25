from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PointViewSet, PointMessageViewSet

router = DefaultRouter()
router.register(r'points', PointViewSet, basename='point')
router.register(r'points/messages', PointMessageViewSet, basename='pointmessage')

urlpatterns = [
    path('', include(router.urls)),
]