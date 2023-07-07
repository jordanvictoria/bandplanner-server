from django.db import models



class PressClipping(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE, related_name='pressclippings')
    title = models.CharField(max_length=200)
    date = models.DateField(blank=True)
    author = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=10000, blank=True)
    link = models.URLField(max_length=200, blank=True)

