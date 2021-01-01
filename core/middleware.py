from fcm_django.models import FCMDevice


class FcmTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and request.user.is_patient and request.path.startswith("/patient/"):
            token = request.headers.get("X-FCM-TOKEN", None)
            if token is not None:
                device = FCMDevice.objects.filter(user=request.user).first()
                if device is None:
                    new_device = FCMDevice(user=request.user, registration_id=token)
                    new_device.save()
                elif device.registration_id != token:
                    device.registration_id = token
                    device.save()
        return response
