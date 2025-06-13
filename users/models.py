from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('administrator', 'Administrator'),
    )
    user_type = models.CharField(
        max_length=15,
        choices=USER_TYPE_CHOICES,
        default='client',
    )
    email = models.EmailField(unique=True) # Ensure email is unique

    # Add any other fields you need for your user model
    # For example, profile picture, bio, etc.

    def __str__(self):
        return self.username
