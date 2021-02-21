from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.models import Doctor, Variable, VariableInstance, Report
from core.serializers import VariableSerializer, ReportSerializer, VariableInstanceSerializer
from doctor.models import PatientInvite
from doctor.permissions import IsDoctor
from doctor.serializers import PatientInviteSerializer
from mailer import mailer
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

    @action(detail=True, methods=['get'])
    def reports(self, request, pk=None):
        patient = self.get_object()
        return Response(ReportSerializer(patient.reports, many=True).data)


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


class InvitesViewSet(mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    permission_classes = [IsDoctor]
    serializer_class = PatientInviteSerializer

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return PatientInvite.objects.filter(doctor=doctor)

    @action(detail=True, methods=['post'])
    def resend(self, request, pk=None):
        invite = self.get_object()
        mailer.send_invite_email(invite)
        return Response(status=status.HTTP_200_OK)


class VariableInstancesViewSet(mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [IsDoctor]
    serializer_class = VariableInstanceSerializer

    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user)
        return VariableInstance.objects.filter(patient__in=doctor.patients.all())
