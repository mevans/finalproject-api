from django.urls import path

from doctor.views import doctor_registration_view, new_patient

urlpatterns = [
    path('auth/register', doctor_registration_view, name="doctor register"),
    path('new-patient', new_patient, name="new patient"),
]
