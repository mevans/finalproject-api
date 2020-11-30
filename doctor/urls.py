from django.urls import path, include
from rest_framework.routers import DefaultRouter

from doctor.view_sets import PatientsViewSet
from doctor.views import DoctorLoginView, DoctorRegistrationView, PatientSignupView, DoctorUserView

router = DefaultRouter()
router.register('patients', PatientsViewSet, basename='patient')

urlpatterns = [
    path('auth/register', DoctorRegistrationView.as_view(), name="doctor register"),
    path('auth/login', DoctorLoginView.as_view(), name="doctor login"),
    path('new-patient', PatientSignupView.as_view(), name="new patient"),
    path('user', DoctorUserView.as_view(), name="doctor user"),
    path('', include(router.urls))
]
