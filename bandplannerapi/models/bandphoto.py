from django.db import models



class BandPhoto(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE, related_name='photos')
    photo = models.CharField(max_length=255, blank=True)
    