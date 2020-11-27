from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Patient
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

        patient = Patient.objects.create(user=user)
        patient.save()

        return Response(data)
