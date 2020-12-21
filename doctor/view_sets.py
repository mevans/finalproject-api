from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Doctor, Variable, VariableInstance, Report
from core.serializers import VariableSerializer, ReportSerializer
from doctor.permissions import IsDoctor
from patient.serializers import PatientSerializer


class PatientsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = PatientSerializer

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return doctor.patients

    @action(detail=True, methods=['post'])
    def link_variable(self, request, pk=None):
        patient = self.get_object()
        variable_id = request.data.pop('variable_id', None)
        if variable_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        variable = Variable.objects.get(id=variable_id)
        variable_instance = VariableInstance.objects.create(patient=patient, variable=variable)
        variable_instance.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlink_variable(self, request, pk=None):
        variable_id = request.data.pop('variable_id', None)
        if variable_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        variable_instance = VariableInstance.objects.get(patient=pk, variable=variable_id)
        variable_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VariablesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = VariableSerializer

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return doctor.variables


class ReportsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = ReportSerializer

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return Report.objects.filter(patient__in=doctor.patients.all())
