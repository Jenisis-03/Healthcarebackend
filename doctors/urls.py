from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, SpecializationViewSet

router = DefaultRouter()
router.register('doctors', DoctorViewSet, basename='doctor')
router.register('specializations', SpecializationViewSet, basename='specialization')

urlpatterns = [
    path('', include(router.urls)),
]