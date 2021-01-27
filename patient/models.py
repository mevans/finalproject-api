from django.db import models

from core.models import Patient


class Theme(models.TextChoices):
    LIGHT = 'LIGHT', "Light"
    DARK = 'DARK', "Dark"


class PatientPreferences(models.Model):
    patient = models.OneToOneField(Patient, related_name="preferences", on_delete=models.CASCADE)

    theme = models.CharField(
        max_length=32,
        choices=Theme.choices,
        default=Theme.LIGHT,
    )
