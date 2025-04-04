from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, AppointmentViewSet, MedicalRecordViewSet
from .mapping_views import PatientDoctorMappingViewSet

router = DefaultRouter()
router.register('patients', PatientViewSet, basename='patient')
router.register('appointments', AppointmentViewSet, basename='appointment')
router.register('medical-records', MedicalRecordViewSet, basename='medical-record')
router.register('mappings', PatientDoctorMappingViewSet, basename='patient-doctor-mapping')

urlpatterns = [
    path('', include(router.urls)),
]