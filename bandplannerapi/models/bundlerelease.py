from django.db import models



class BundleRelease(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE, related_name='bundlereleases')
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='bundlereleases')
    bundle_title = models.CharField(max_length=50)
    genre = models.CharField(max_length=50, blank=True)
    upc = models.IntegerField(blank=True)
    audio_url = models.URLField(max_length=200, blank=True)
    artwork =  models.CharField(max_length=255, blank=True)
    uploaded_to_distro = models.BooleanField(default=False)
