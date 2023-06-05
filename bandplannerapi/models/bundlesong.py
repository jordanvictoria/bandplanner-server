from django.db import models



class BundleSong(models.Model):

    bundle = models.ForeignKey("BundleRelease", on_delete=models.CASCADE, related_name='bundlereleases')
    song_title = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    isrc = models.IntegerField(blank=True)
    release_date = models.DateField()
    composer = models.CharField(max_length=50)
    producer = models.CharField(max_length=50)
    explicit = models.BooleanField()
