from dj_rest_auth.views import LoginView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core.models import Doctor
from core.views import RegistrationView
from doctor.models import PatientSignupToken
from doctor.permissions import IsDoctor
from doctor.serializers import DoctorRegistrationSerializer, PatientSignupTokenSerializer, DoctorLoginSerializer


class DoctorRegistrationView(RegistrationView):
    serializer_class = DoctorRegistrationSerializer


@api_view(['GET'])
@permission_classes([IsDoctor])
def new_patient(request):
    doctor = Doctor.objects.get(user=request.user)
    signup_token = PatientSignupToken.objects.create(doctor=doctor)
    serializer = PatientSignupTokenSerializer(signup_token)
    return Response(serializer.data)


class DoctorLoginView(LoginView):
    serializer_class = DoctorLoginSerializer
