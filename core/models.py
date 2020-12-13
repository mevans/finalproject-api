from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


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


class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reports')
    date = models.DateTimeField(auto_now_add=True)


class Variable(models.Model):
    name = models.CharField('name', max_length=150)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='variables')

    def __str__(self):
        return '({}) {}'.format(self.id, self.name)


class VariableInstance(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE)

    def __str__(self):
        return '({}) Patient: {}, Variable: {}'.format(self.id, self.patient, self.variable)


class AbstractVariableType(models.Model):
    variable = models.OneToOneField(Variable, on_delete=models.CASCADE, related_name='type')

    class Meta:
        abstract = True


class RangeVariableType(AbstractVariableType):
    min_value = models.PositiveIntegerField(default=1, blank=False, null=False)
    max_value = models.PositiveIntegerField(default=5, blank=False, null=False)


class AbstractVariableResponse(models.Model):
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class RangeVariableTypeResponse(AbstractVariableResponse):
    response = models.PositiveIntegerField(blank=False)
