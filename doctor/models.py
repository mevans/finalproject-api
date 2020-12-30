from django.db import models
from django.utils.crypto import get_random_string

from core.models import Doctor


class PatientSignupToken(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=5)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    first_name = models.CharField('first name', max_length=150, blank=True)
    last_name = models.CharField('last_name', max_length=150, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.id = get_random_string(length=5, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ' '0123456789')
        super().save(force_insert, force_update, using, update_fields)
