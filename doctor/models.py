from django.db import models
# Create your models here.
from shortuuidfield import ShortUUIDField

from core.models import Doctor


class PatientSignupToken(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, max_length=8)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    first_name = models.CharField('first name', max_length=150, blank=True)
    last_name = models.CharField('last_name', max_length=150, blank=True)
