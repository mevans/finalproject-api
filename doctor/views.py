from dj_rest_auth.views import LoginView
from rest_framework.generics import CreateAPIView

from core.views import RegistrationView
from doctor.permissions import IsDoctor
from doctor.serializers import DoctorRegistrationSerializer, PatientSignupTokenSerializer, DoctorLoginSerializer


class DoctorRegistrationView(RegistrationView):
    serializer_class = DoctorRegistrationSerializer


class PatientSignupView(CreateAPIView):
    serializer_class = PatientSignupTokenSerializer
    permission_classes = [IsDoctor]

    def post(self, request, *args, **kwargs):
        request.data['doctor'] = request.user
        return super().create(request, *args, **kwargs)


class DoctorLoginView(LoginView):
    serializer_class = DoctorLoginSerializer
