from rest_framework import viewsets

from core.models import Doctor
from core.serializers import VariableSerializer
from doctor.permissions import IsDoctor
from patient.serializers import PatientSerializer


class PatientsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = PatientSerializer

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return doctor.patients


class VariablesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = VariableSerializer

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return doctor.variables
