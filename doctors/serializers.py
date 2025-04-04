from rest_framework import serializers
from .models import Doctor, Specialization
from authentication.models import User

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name', 'description']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth']
        read_only_fields = ['username']

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    specialization = SpecializationSerializer(read_only=True)
    specialization_id = serializers.PrimaryKeyRelatedField(
        queryset=Specialization.objects.all(),
        write_only=True,
        source='specialization'
    )
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'full_name', 'specialization', 'specialization_id',
                 'license_number', 'experience_years', 'consultation_fee',
                 'available_days', 'available_time_start', 'available_time_end']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.get(id=self.context['request'].user.id)
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

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

    def validate_available_days(self, value):
        """Validate the format of available_days"""
        days = [day.strip() for day in value.split(',')]
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in days:
            if day not in valid_days:
                raise serializers.ValidationError(
                    f"Invalid day format. Use comma-separated full day names: {', '.join(valid_days)}"
                )
        return value