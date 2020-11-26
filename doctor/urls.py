from django.urls import path

from doctor.views import doctor_registration_view

urlpatterns = [
    path('auth/register', doctor_registration_view, name="doctor register")
]
