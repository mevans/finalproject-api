from dj_rest_auth.app_settings import LoginSerializer
from rest_framework import serializers, exceptions

from core.models import User
from doctor.models import PatientSignupToken


class PatientRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'token']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_token(self, value):
        try:
            PatientSignupToken.objects.get(id=value)
        except PatientSignupToken.DoesNotExist:
            raise serializers.ValidationError('Invalid token')
        return value

    def save(self):
        user = User(email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        user.set_password(password)
        user.save()
        return user


class PatientLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        validated = super().validate(attrs)
        user = validated['user']
        if not user.is_patient:
            raise exceptions.ValidationError("Only patients can login to this site")
        return validated
