from django.contrib import admin

# Register your models here.
from doctor.models import PatientSignupToken

admin.site.register(PatientSignupToken)
