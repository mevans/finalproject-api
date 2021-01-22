from datetime import datetime, timedelta

import jwt
from django.db import models
from django.utils.crypto import get_random_string

from core.models import Doctor
from dynamic_links import dynamic_links
from tracker import settings


class PatientInvite(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=5)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    first_name = models.CharField('first name', max_length=150, blank=False)
    last_name = models.CharField('last_name', max_length=150, blank=False)
    email = models.EmailField('email', null=True, unique=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.id = get_random_string(length=5, allowed_chars='ABCDEFGHJKMNPQRSTUVWXYZ' '123456789')
        super().save(force_insert, force_update, using, update_fields)

    def generate_verify_token(self):
        claims = {
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=1),
            'code': self.id,
        }
        token = jwt.encode(claims, settings.SECRET_KEY, algorithm="HS256")
        return token

    def generate_link(self):
        token = self.generate_verify_token()
        return dynamic_links.generate_invite_link(token)
