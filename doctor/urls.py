from django.urls import path

from doctor.views import new_patient, DoctorLoginView, DoctorRegistrationView

urlpatterns = [
    path('auth/register', DoctorRegistrationView.as_view(), name="doctor register"),
    path('auth/login', DoctorLoginView.as_view(), name="doctor login"),
    path('new-patient', new_patient, name="new patient"),
]
