from dj_rest_auth.views import LoginView

from core.views import RegistrationView
from patient.serializers import PatientRegistrationSerializer, PatientLoginSerializer


class PatientRegistrationView(RegistrationView):
    serializer_class = PatientRegistrationSerializer


class PatientLoginView(LoginView):
    serializer_class = PatientLoginSerializer
