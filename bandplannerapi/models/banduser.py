from django.db import models
from django.contrib.auth.models import User


class BandUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=50)
    bio = models.CharField(max_length=50, blank=True, null=True)
    streaming = models.URLField(max_length=200, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    tiktok = models.URLField(max_length=200, blank=True, null=True)

    @property
    def full_name(self):
        """."""
        return f'{self.user.first_name} {self.user.last_name}'
        
        