from rest_framework import viewsets

from core.models import Doctor
from doctor.permissions import IsDoctor
from patient.serializers import PatientSerializer


class PatientsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = PatientSerializer

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return doctor.patients
