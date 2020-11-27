from django.urls import path

from patient.views import patient_registration_view

urlpatterns = [
    path('auth/register', patient_registration_view, name="patient register"),
]
