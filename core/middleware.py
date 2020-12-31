class FcmTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path.startswith("/patient/"):
            token = request.headers.get("X-FCM-TOKEN", None)
            if token is not None:
                patient = request.user.patient
                patient.fcm_token = token
                patient.save()
        response = self.get_response(request)
        return response
