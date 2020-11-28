from dj_rest_auth.app_settings import LoginSerializer
from rest_framework import serializers, exceptions

from core.models import Patient
from core.serializers import RegistrationSerializer
from doctor.models import PatientSignupToken


class PatientRegistrationSerializer(RegistrationSerializer):
    token = serializers.CharField(write_only=True)

    class Meta(RegistrationSerializer.Meta):
        fields = ['email', 'password', 'password2', 'token']

    def validate_token(self, value):
        try:
            PatientSignupToken.objects.get(id=value)
        except PatientSignupToken.DoesNotExist:
            raise serializers.ValidationError('Invalid token')
        return value

    def handle_save(self, user):
        user.is_patient = True
        super().handle_save(user)
        token = PatientSignupToken.objects.get(id=self.validated_data['token'])

        patient = Patient.objects.create(user=user, doctor=token.doctor)
        patient.save()

        token.delete()


class PatientLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        validated = super().validate(attrs)
        user = validated['user']
        if not user.is_patient:
            raise exceptions.ValidationError("Only patients can login to this site")
        return validated
