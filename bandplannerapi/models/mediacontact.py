from django.db import models



class MediaContact(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE, related_name='mediacontacts')
    organization = models.CharField(max_length=50)
    contact = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254)
    website = models.URLField(max_length=200, blank=True)
    notes = models.TextField(max_length=500, blank=True)
    media_type = models.ForeignKey("MediaType", on_delete=models.CASCADE, related_name='mediacontacts')

    