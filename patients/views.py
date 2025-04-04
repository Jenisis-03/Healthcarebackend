from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Patient, Appointment, MedicalRecord
from doctors.models import Doctor
from .serializers import PatientSerializer, AppointmentSerializer, MedicalRecordSerializer

class IsPatientOrDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type in ['PATIENT', 'DOCTOR']

class IsPatientOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsDoctorForAppointment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.user_type == 'DOCTOR' and obj.doctor.user == request.user

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'DOCTOR':
            # Doctors can see patients they have appointments with
            return Patient.objects.filter(appointments__doctor__user=self.request.user).distinct()
        elif self.request.user.user_type == 'PATIENT':
            # Patients can only see their own profile
            return Patient.objects.filter(user=self.request.user)
        return Patient.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOrDoctor]

    def get_queryset(self):
        if self.request.user.user_type == 'DOCTOR':
            return Appointment.objects.filter(doctor__user=self.request.user)
        elif self.request.user.user_type == 'PATIENT':
            return Appointment.objects.filter(patient__user=self.request.user)
        return Appointment.objects.none()

    def perform_create(self, serializer):
        if self.request.user.user_type == 'PATIENT':
            patient = get_object_or_404(Patient, user=self.request.user)
            serializer.save(patient=patient)
        else:
            serializer.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        if appointment.status != 'SCHEDULED':
            return Response(
                {"error": "Only scheduled appointments can be cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        appointment.status = 'CANCELLED'
        appointment.save()
        return Response(AppointmentSerializer(appointment).data)

class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'DOCTOR':
            return MedicalRecord.objects.filter(doctor__user=self.request.user)
        elif self.request.user.user_type == 'PATIENT':
            return MedicalRecord.objects.filter(patient__user=self.request.user)
        return MedicalRecord.objects.none()

    def perform_create(self, serializer):
        if self.request.user.user_type == 'DOCTOR':
            doctor = get_object_or_404(Doctor, user=self.request.user)
            serializer.save(doctor=doctor)
        else:
            serializer.save()
