from django.urls import path

from doctor.views import DoctorLoginView, DoctorRegistrationView, PatientSignupView

urlpatterns = [
    path('auth/register', DoctorRegistrationView.as_view(), name="doctor register"),
    path('auth/login', DoctorLoginView.as_view(), name="doctor login"),
    path('new-patient', PatientSignupView.as_view(), name="new patient"),
]
