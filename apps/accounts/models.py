from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Extends the default Django User model.
    We are not adding any extra fields for now, but this setup
    allows us to easily add them in the future without a complex migration.
    For example: email_verified = models.BooleanField(default=False)
    """
    def __str__(self):
        return self.username
