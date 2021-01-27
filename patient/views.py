import jwt
from dj_rest_auth.views import LoginView
from rest_framework import status, mixins
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from core.models import Patient, VariableNotificationPreference
from core.serializers import ReportSerializer, VariableInstanceSerializer, VariableNotificationPreferenceSerializer
from core.views import RegistrationView
from doctor.models import PatientInvite
from doctor.serializers import PatientInviteSerializer
from patient.permissions import IsPatient
from patient.serializers import PatientRegistrationSerializer, PatientLoginSerializer, PatientSerializer, \
    PatientPreferencesSerializer
from tracker import settings


class PatientVerifyInviteCodeView(APIView):
    def post(self, request):
        code = request.data.get('code', None)
        try:
            invite = PatientInvite.objects.get(id=code)
            return Response(data=PatientInviteSerializer(invite).data)
        except PatientInvite.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PatientVerifyInviteTokenView(APIView):
    def post(self, request):
        unverified_token = request.data.get('token', None)
        try:
            decoded = jwt.decode(unverified_token, settings.SECRET_KEY, algorithms=["HS256"])
            code = decoded.get('code')
            invite = PatientInvite.objects.get(id=code)
            return Response(data=PatientInviteSerializer(invite).data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PatientRegistrationView(RegistrationView):
    serializer_class = PatientRegistrationSerializer


class PatientLoginView(LoginView):
    serializer_class = PatientLoginSerializer


class PatientUserView(RetrieveAPIView):
    serializer_class = PatientSerializer

    permission_classes = [IsPatient]

    def get_object(self):
        return Patient.objects.get(user=self.request.user)


class VariablesView(ListAPIView):
    serializer_class = VariableInstanceSerializer

    permission_classes = [IsPatient]

    def get_queryset(self):
        patient = self.request.user.patient
        return patient.variableinstance_set


class SubmitReport(CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsPatient]


class VariableNotificationPreferencesView(mixins.ListModelMixin,
                                          mixins.UpdateModelMixin,
                                          GenericViewSet):
    serializer_class = VariableNotificationPreferenceSerializer
    permission_classes = [IsPatient]

    def get_queryset(self):
        patient = self.request.user.patient
        return VariableNotificationPreference.objects.filter(instance__patient=patient)


class PatientPreferencesView(APIView):
    permission_classes = [IsPatient]

    def get(self, request):
        patient = request.user.patient
        preferences = patient.preferences
        return Response(PatientPreferencesSerializer(preferences).data)

    def patch(self, request):
        patient = request.user.patient
        serializer = PatientPreferencesSerializer(patient.preferences, data=request.data)
        serializer.is_valid(raise_exception=True)
        preferences = serializer.save()
        return Response(PatientPreferencesSerializer(preferences).data)
