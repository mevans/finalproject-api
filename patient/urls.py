from django.urls import path

from patient.views import PatientLoginView, PatientRegistrationView

urlpatterns = [
    path('auth/register', PatientRegistrationView.as_view(), name="patient register"),
    path('auth/login', PatientLoginView.as_view(), name="patient login"),
]
