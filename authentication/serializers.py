from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from patients.models import Patient
from doctors.models import Doctor

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email', 'first_name', 
                 'last_name', 'phone_number', 'address', 'date_of_birth', 'user_type']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Create associated profile based on user type
        if user.user_type == 'PATIENT':
            Patient.objects.create(user=user)
        elif user.user_type == 'DOCTOR':
            raise serializers.ValidationError(
                "Doctor registration requires additional profile information. "
                "Please use the doctor profile endpoint to complete registration."
            )

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'phone_number', 'address', 'date_of_birth', 'user_type']
        read_only_fields = ['username', 'user_type']