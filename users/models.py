from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_designer = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True)  # Example field for storing social media links
