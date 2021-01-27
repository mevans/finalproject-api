from dj_rest_auth.app_settings import LoginSerializer
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers, exceptions

from core.models import Patient
from core.serializers import RegistrationSerializer, UserSerializer, VariableInstanceSerializer
from doctor.models import PatientInvite
from doctor.serializers import DoctorSerializer
from patient.models import PatientPreferences


class PatientSerializer(FlexFieldsModelSerializer):
    user = UserSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    instances = serializers.PrimaryKeyRelatedField(source='get_instances', many=True, read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
        expandable_fields = {
            'instances': (VariableInstanceSerializer, {'many': True, 'source': 'get_instances'})
        }

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
    code = serializers.CharField(write_only=True)

    class Meta(RegistrationSerializer.Meta):
        fields = ['email', 'password', 'password2', 'code']

    def validate_code(self, value):
        try:
            PatientInvite.objects.get(id=value)
        except PatientInvite.DoesNotExist:
            raise serializers.ValidationError('Invalid code')
        return value

    def handle_save(self, user):
        user.is_patient = True
        super().handle_save(user)
        invite = PatientInvite.objects.get(id=self.validated_data['code'])
        user.first_name = invite.first_name
        user.last_name = invite.last_name
        user.save()

        patient = Patient.objects.create(user=user, doctor=invite.doctor)
        patient.save()

        invite.delete()


class PatientLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        validated = super().validate(attrs)
        user = validated['user']
        if not user.is_patient:
            raise exceptions.ValidationError("Only patients can login to this site")
        return validated


class PatientPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientPreferences
        fields = '__all__'
        read_only_fields = ['patient']
