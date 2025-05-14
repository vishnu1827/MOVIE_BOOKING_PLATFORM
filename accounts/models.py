from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    phone = models.IntegerField(unique=True , null=True, blank=True)
    is_theatre_manager = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    otp = models.CharField(null=True, blank=True)
    otp_verified = models.BooleanField(default=False)
    

