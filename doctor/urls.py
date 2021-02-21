from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from doctor.view_sets import PatientsViewSet, VariablesViewSet, ReportsViewSet, InvitesViewSet, VariableInstancesViewSet
from doctor.views import DoctorLoginView, DoctorRegistrationView, PatientSignupView, DoctorUserView, DoctorLogoutView

router = DefaultRouter()
router.register('patients', PatientsViewSet, basename='patient')
router.register('variables', VariablesViewSet, basename='variable')
router.register('reports', ReportsViewSet, basename='report')
router.register('invites', InvitesViewSet, basename='invite')
router.register('variable-instances', VariableInstancesViewSet, basename='variable-instance')

urlpatterns = [
    path('auth/register', DoctorRegistrationView.as_view(), name="doctor register"),
    path('auth/login', DoctorLoginView.as_view(), name="doctor login"),
    path('auth/logout', DoctorLogoutView.as_view(), name="doctor logout"),
    path('auth/refresh-token', TokenRefreshView.as_view(), name="doctor refresh token"),
    path('new-patient', PatientSignupView.as_view(), name="new patient"),
    path('user', DoctorUserView.as_view(), name="doctor user"),
    path('', include(router.urls))
]
