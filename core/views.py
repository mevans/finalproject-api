from dj_rest_auth.app_settings import JWTSerializer
from dj_rest_auth.utils import jwt_encode
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response


class RegistrationView(CreateAPIView):
    def get_response_data(self, user, access_token, refresh_token):
        data = {
            'user': user,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return JWTSerializer(data, context=self.get_serializer_context()).data

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        access_token, refresh_token = jwt_encode(user)
        response = self.get_response_data(user, access_token, refresh_token)
        return Response(response, status=status.HTTP_201_CREATED)
