from dj_rest_auth.views import LoginView
from rest_framework.generics import RetrieveAPIView

from core.models import Patient
from core.views import RegistrationView
from patient.permissions import IsPatient
from patient.serializers import PatientRegistrationSerializer, PatientLoginSerializer, PatientSerializer


class PatientRegistrationView(RegistrationView):
    serializer_class = PatientRegistrationSerializer


class PatientLoginView(LoginView):
    serializer_class = PatientLoginSerializer


class PatientUserView(RetrieveAPIView):
    serializer_class = PatientSerializer

    permission_classes = [IsPatient]

    def get_object(self):
        return Patient.objects.get(user=self.request.user)
