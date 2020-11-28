from django.urls import path

from patient.views import patient_registration_view, PatientLoginView

urlpatterns = [
    path('auth/register', patient_registration_view, name="patient register"),
    path('auth/login', PatientLoginView.as_view(), name="patient login"),
]
