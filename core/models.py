import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import DateTimeField
from recurrence.fields import RecurrenceField

from core.utils import rebuild_notifications


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    username = None
    email = models.EmailField('Email Address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return '({}) {}'.format(self.user.id, self.user.email)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patients')
    variables = models.ManyToManyField('Variable', through='VariableInstance')

    def __str__(self):
        return '({}) {}'.format(self.user.id, self.user.email)

    def get_instances(self):
        return VariableInstance.objects.filter(patient=self)


class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reports')
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)

    def get_range_responses(self):
        return RangeVariableTypeResponse.objects.filter(report=self)

    def get_choice_responses(self):
        return ChoiceVariableTypeResponse.objects.filter(report=self)


class Variable(models.Model):
    name = models.CharField('name', max_length=150)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='variables')

    def __str__(self):
        return '({}) {}'.format(self.id, self.name)

    def get_range(self):
        try:
            return RangeVariableType.objects.get(variable=self)
        except RangeVariableType.DoesNotExist:
            return None

    def get_choice(self):
        try:
            return ChoiceVariableType.objects.get(variable=self)
        except ChoiceVariableType.DoesNotExist:
            return None

    def get_used_by(self):
        return Patient.objects.filter(variableinstance__variable__exact=self)


class VariableInstance(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE)
    schedule = RecurrenceField(null=True)

    def __str__(self):
        return '({}) Patient: {}, Variable: {}'.format(self.id, self.patient, self.variable)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(VariableInstance, self).save(*args, **kwargs)
        if created:
            self.add_notification_preference()
        rebuild_notifications(self)

    def add_notification_preference(self):
        preference = VariableNotificationPreference(instance=self)
        preference.save()


class AbstractVariableType(models.Model):
    variable = models.OneToOneField(Variable, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class RangeVariableType(AbstractVariableType):
    min_value = models.PositiveIntegerField(default=1, blank=False, null=False)
    max_value = models.PositiveIntegerField(default=5, blank=False, null=False)


class ChoiceVariableType(AbstractVariableType):
    pass


class ChoiceVariableChoice(models.Model):
    choice_type = models.ForeignKey(ChoiceVariableType, on_delete=models.CASCADE, related_name='choices')
    value = models.CharField(max_length=150, blank=False, null=False)


class AbstractVariableResponse(models.Model):
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class RangeVariableTypeResponse(AbstractVariableResponse):
    response = models.PositiveIntegerField(blank=False)


class ChoiceVariableTypeResponse(AbstractVariableResponse):
    response = models.ForeignKey(ChoiceVariableChoice, on_delete=models.CASCADE)


class VariableNotification(models.Model):
    scheduled_for = DateTimeField()
    instance = models.ForeignKey(VariableInstance, on_delete=models.CASCADE)


class VariableNotificationPreference(models.Model):
    instance = models.OneToOneField(VariableInstance, on_delete=models.CASCADE, related_name="notification_preference")
    time = models.TimeField(null=False, default=datetime.time(17, 00))
    enabled = models.BooleanField(null=False, default=True)

    def save(self, *args, **kwargs):
        super(VariableNotificationPreference, self).save(*args, **kwargs)
        if self.enabled:
            rebuild_notifications(self.instance)
        else:
            VariableNotification.objects.filter(instance=self.instance).delete()
