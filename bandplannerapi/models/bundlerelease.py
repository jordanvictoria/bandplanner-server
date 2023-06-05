from django.db import models



class BundleRelease(models.Model):

    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='singlereleases')
    bundle_title = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    upc = models.IntegerField(blank=True)
    release_date = models.DateField()
    audio_url = models.URLField(max_length=200, blank=True)
    artwork =  models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    uploaded_to_distro = models.BooleanField()
