from dj_rest_auth.app_settings import LoginSerializer
from rest_framework import serializers, exceptions

from core.models import Doctor
from core.serializers import RegistrationSerializer
from doctor.models import PatientSignupToken


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class DoctorRegistrationSerializer(RegistrationSerializer):
    def handle_save(self, user):
        user.is_doctor = True
        super().handle_save(user)
        doctor = Doctor.objects.create(user=user)
        doctor.save()


class PatientSignupTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSignupToken
        fields = '__all__'


class DoctorLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        validated = super().validate(attrs)
        user = validated['user']
        if not user.is_doctor:
            raise exceptions.ValidationError("Only doctors can login to this site")
        return validated
