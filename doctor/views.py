from dj_rest_auth.app_settings import LoginSerializer
from dj_rest_auth.views import LoginView
from rest_framework import exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core.models import Doctor
from doctor.models import PatientSignupToken
from doctor.permissions import IsDoctor
from doctor.serializers import RegistrationSerializer, PatientSignupTokenSerializer, DoctorLoginSerializer


@api_view(['POST'])
def doctor_registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if not serializer.is_valid():
            data = serializer.errors
            return Response(data)

        user = serializer.save()
        user.is_doctor = True
        user.save()
        data['response'] = "Successfully registered a new doctor"
        data['email'] = user.email

        doctor = Doctor.objects.create(user=user)
        doctor.save()

        return Response(data)


@api_view(['GET'])
@permission_classes([IsDoctor])
def new_patient(request):
    doctor = Doctor.objects.get(user=request.user)
    signup_token = PatientSignupToken.objects.create(doctor=doctor)
    serializer = PatientSignupTokenSerializer(signup_token)
    return Response(serializer.data)


class DoctorLoginView(LoginView):
    serializer_class = DoctorLoginSerializer
