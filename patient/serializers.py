from dj_rest_auth.app_settings import LoginSerializer
from rest_framework import serializers, exceptions

from core.models import Patient
from core.serializers import RegistrationSerializer, UserSerializer
from doctor.models import PatientSignupToken
from doctor.serializers import DoctorSerializer


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = representation.pop('user')
        for key in user_representation:
            representation[key] = user_representation[key]
        return representation

    def update(self, instance, validated_data):
        user_fields = ['first_name', 'last_name']
        for field in user_fields:
            value = validated_data.pop(field, None)
            if value is not None:
                setattr(instance.user, field, value)
        instance.user.save()
        return super().update(instance, validated_data)


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
        user.first_name = token.first_name
        user.last_name = token.last_name
        user.save()

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
