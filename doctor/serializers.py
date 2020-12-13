from dj_rest_auth.app_settings import LoginSerializer
from rest_framework import serializers, exceptions

from core.models import Doctor
from core.serializers import RegistrationSerializer, UserSerializer
from doctor.models import PatientSignupToken


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = representation.pop('user')
        for key in user_representation:
            representation[key] = user_representation[key]
        return representation

class DoctorRegistrationSerializer(RegistrationSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta(RegistrationSerializer.Meta):
        fields = [*RegistrationSerializer.Meta.fields, 'first_name', 'last_name']

    def handle_save(self, user):
        user.is_doctor = True
        user.first_name = self.validated_data['first_name']
        user.last_name = self.validated_data['last_name']
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
