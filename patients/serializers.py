from rest_framework import serializers
from .models import Patient, Appointment, MedicalRecord
from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth']
        read_only_fields = ['username']

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'blood_group', 'allergies', 'medical_conditions', 
                 'emergency_contact_name', 'emergency_contact_number']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.get(id=self.context['request'].user.id)
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        patient = Patient.objects.create(user=user, **validated_data)
        return patient

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'patient_name', 'doctor_name', 
                 'appointment_date', 'appointment_time', 'status', 'reason', 
                 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """Validate appointment scheduling"""
        doctor = data.get('doctor')
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time')

        # Check if the doctor is available on the given date and time
        if doctor and appointment_date and appointment_time:
            # Convert appointment time to string for comparison
            appointment_time_str = appointment_time.strftime('%H:%M:%S')
            if appointment_time_str < doctor.available_time_start.strftime('%H:%M:%S') or \
               appointment_time_str > doctor.available_time_end.strftime('%H:%M:%S'):
                raise serializers.ValidationError("Appointment time is outside doctor's available hours")

            # Check for existing appointments
            existing_appointments = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status='SCHEDULED'
            ).exists()

            if existing_appointments:
                raise serializers.ValidationError("This time slot is already booked")

        return data

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'patient_name', 'doctor_name', 
                 'diagnosis', 'prescription', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']