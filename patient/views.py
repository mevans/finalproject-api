from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Patient
from doctor.models import PatientSignupToken
from patient.serializers import PatientRegistrationSerializer


@api_view(['POST'])
def patient_registration_view(request):
    if request.method == 'POST':
        serializer = PatientRegistrationSerializer(data=request.data)
        data = {}

        if not serializer.is_valid():
            data = serializer.errors
            return Response(data)

        user = serializer.save()
        user.is_patient = True
        user.save()
        data['response'] = "Successfully registered a new patient"
        data['email'] = user.email

        token = PatientSignupToken.objects.get(id=serializer.validated_data['token'])
        token.delete()
        doctor = token.doctor
        data['doctor'] = doctor.pk

        patient = Patient.objects.create(user=user, doctor=token.doctor)
        patient.save()

        return Response(data)
