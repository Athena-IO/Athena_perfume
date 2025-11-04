from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_wholesaler = models.BooleanField(default=False)  # مشتری عمده فروش است یا خیر؟
    company_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return f"{self.company_name or self.username}"

