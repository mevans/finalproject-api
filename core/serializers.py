from rest_framework import serializers

from core.models import User, Patient


class JWTSerializer(serializers.Serializer):
    access = serializers.CharField(source='access_token')
    refresh = serializers.CharField(source='refresh_token')


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def handle_save(self, user):
        user.save()

    def save(self):
        user = User(email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        user.set_password(password)
        self.handle_save(user)
        return user
