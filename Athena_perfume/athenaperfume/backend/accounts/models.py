from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # optional phone field (unique)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.username or self.phone} ({self.role})"
