from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Doctor
from doctor.serializers import RegistrationSerializer


@api_view(['POST'])
def doctor_registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if not serializer.is_valid():
            data = serializer.errors
            return Response(data)

        user = serializer.save()
        user.is_doctor = True
        user.save()
        data['response'] = "Successfully registered a new doctor"
        data['email'] = user.email

        doctor = Doctor.objects.create(user=user)
        doctor.save()

        return Response(data)
