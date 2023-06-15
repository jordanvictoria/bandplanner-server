from django.db import models



class BundleSong(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE, related_name='bundlesongs')
    bundle = models.ForeignKey("BundleRelease", on_delete=models.CASCADE, related_name='bundlesongs')
    song_title = models.CharField(max_length=50)
    genre = models.CharField(max_length=50, blank=True)
    isrc = models.IntegerField(blank=True)
    composer = models.CharField(max_length=50, blank=True)
    producer = models.CharField(max_length=50, blank=True)
    explicit = models.BooleanField()
