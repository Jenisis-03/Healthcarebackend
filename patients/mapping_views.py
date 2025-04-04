from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Patient, PatientDoctorMapping
from doctors.models import Doctor
from .mapping_serializers import PatientDoctorMappingSerializer

class IsPatientOrDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type in ['PATIENT', 'DOCTOR']

class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOrDoctor]

    def get_queryset(self):
        if self.request.user.user_type == 'DOCTOR':
            return PatientDoctorMapping.objects.filter(doctor__user=self.request.user)
        elif self.request.user.user_type == 'PATIENT':
            return PatientDoctorMapping.objects.filter(patient__user=self.request.user)
        return PatientDoctorMapping.objects.none()

    def perform_create(self, serializer):
        if self.request.user.user_type == 'PATIENT':
            patient = get_object_or_404(Patient, user=self.request.user)
            doctor = get_object_or_404(Doctor, id=self.request.data.get('doctor_id'))
            serializer.save(patient=patient, doctor=doctor)
        elif self.request.user.user_type == 'DOCTOR':
            doctor = get_object_or_404(Doctor, user=self.request.user)
            patient = get_object_or_404(Patient, id=self.request.data.get('patient_id'))
            serializer.save(patient=patient, doctor=doctor)