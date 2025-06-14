from rest_framework import serializers
from .models import User, OTP

class SendOTPSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=5, default='+91')
    phone_number = serializers.CharField(max_length=10)

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError('Phone number must be 10 digits')
        return value

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'country_code', 'full_name', 'date_of_birth', 'time_of_birth', 'gender']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'date_of_birth', 'time_of_birth', 'gender']
        extra_kwargs = {
            'full_name': {'required': True},
            'date_of_birth': {'required': True},
            'time_of_birth': {'required': True},
            'gender': {'required': True},
        }