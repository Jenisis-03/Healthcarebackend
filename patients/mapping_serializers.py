from rest_framework import serializers
from .models import PatientDoctorMapping
from doctors.serializers import DoctorSerializer
from .serializers import PatientSerializer

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(source='patient', read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient_id', 'doctor_id', 'patient_details', 'doctor_details', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        request = self.context.get('request')
        if request and request.user:
            if request.user.user_type == 'PATIENT':
                if not data.get('doctor'):
                    raise serializers.ValidationError("Doctor ID is required")
            elif request.user.user_type == 'DOCTOR':
                if not data.get('patient'):
                    raise serializers.ValidationError("Patient ID is required")
        return data