<<<<<<< HEAD
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_wholesaler = models.BooleanField(default=False)#مشتری عمده فروش است یا خیر؟
    company_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=False)
 
def __str__(self):
 return f'{self.company_name}'
=======
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


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


# -------------------------
# مدل ثبت لاگ‌های ورود
# -------------------------
class LoginLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    username_attempt = models.CharField(max_length=150)
    ip_address = models.CharField(max_length=50)
    user_agent = models.TextField()
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username_attempt} - {'Success' if self.success else 'Failed'} - {self.timestamp}"
>>>>>>> f269ab4 (Initial commit - Django project with MySQL setup)
