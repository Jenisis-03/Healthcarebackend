from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Doctor, Specialization
from .serializers import DoctorSerializer, SpecializationSerializer

class IsDoctorOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Doctor.objects.all()
        specialization = self.request.query_params.get('specialization', None)
        if specialization is not None:
            queryset = queryset.filter(specialization_id=specialization)
        return queryset

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsDoctorOwner()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        doctor = self.get_object()
        return Response({
            'available_days': doctor.available_days.split(','),
            'available_time_start': doctor.available_time_start,
            'available_time_end': doctor.available_time_end
        })

    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        doctor = self.get_object()
        appointments = doctor.appointments.filter(status='SCHEDULED')
        from patients.serializers import AppointmentSerializer
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
