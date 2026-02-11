from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TravelProjectViewSet, ProjectPlaceViewSet

router = DefaultRouter()
router.register(r'projects', TravelProjectViewSet, basename='project')
router.register(r'places', ProjectPlaceViewSet, basename='place')

urlpatterns = [
    path('', include(router.urls)),
]