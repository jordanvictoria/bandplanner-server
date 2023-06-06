from django.db import models



class SingleRelease(models.Model):

    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='singlereleases')
    song_title = models.CharField(max_length=50)
    genre = models.CharField(max_length=50, blank=True)
    upc = models.IntegerField(blank=True)
    isrc = models.IntegerField(blank=True)
    composer = models.CharField(max_length=50, blank=True)
    producer = models.CharField(max_length=50, blank=True)
    explicit = models.BooleanField()
    audio_url = models.URLField(max_length=200, blank=True)
    artwork =  models.CharField(max_length=255, blank=True)
    uploaded_to_distro = models.BooleanField(default=False)
