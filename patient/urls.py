from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from patient.views import PatientLoginView, PatientRegistrationView, PatientUserView, SubmitReport, VariablesView

urlpatterns = [
    path('auth/register', PatientRegistrationView.as_view(), name="patient register"),
    path('auth/login', PatientLoginView.as_view(), name="patient login"),
    path('auth/refresh-token', TokenRefreshView.as_view(), name="patient refresh token"),
    path('user', PatientUserView.as_view(), name="patient user"),
    path('report', SubmitReport.as_view(), name="submit report"),
    path('variables', VariablesView.as_view(), name="patient variables")
]
