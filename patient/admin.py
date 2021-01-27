from django.contrib import admin

# Register your models here.
from patient.models import PatientPreferences

admin.site.register(PatientPreferences)
