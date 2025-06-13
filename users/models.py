from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import DateTimeField

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
    last_logout_time = models.DateTimeField(null=True, blank=True)

    # Add any other fields you need for your user model
    # For example, profile picture, bio, etc.

    def __str__(self):
        return self.username

    def get_last_session_duration(self):
        """
        Calculates the duration of the last session based on last_login and last_logout_time.

        Returns:
            timedelta: The duration of the last session if calculable.
            None: If last_login or last_logout_time is not set, or if last_logout_time
                  is not greater than last_login.
        """
        if self.last_login and self.last_logout_time:
            if self.last_logout_time > self.last_login:
                return self.last_logout_time - self.last_login
        return None
