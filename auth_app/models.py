
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.utils import timezone

class FocusArea(models.Model):
    FOCUS_AREA_CHOICES = [
        ('H', 'Health'),
        ('W', 'Wealth'),
        ('R', 'Relationships'),
        ('C', 'Career'),
        ('S', 'Spirituality'),
    ]
    name = models.CharField(max_length=1, choices=FOCUS_AREA_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class UserManager(BaseUserManager):
    def create_user(self, phone_number, country_code='+91', password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, country_code=country_code, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, country_code='+91', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, country_code, password, **extra_fields)

class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    country_code = models.CharField(max_length=5, default='+91')
    full_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    time_of_birth = models.TimeField(null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    focus_area = models.CharField(max_length=1, choices=FocusArea.FOCUS_AREA_CHOICES, blank=True)

    # Required fields for Django authentication
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['country_code']

    def __str__(self):
        return f"{self.country_code}{self.phone_number}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

class OTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.phone_number}"
