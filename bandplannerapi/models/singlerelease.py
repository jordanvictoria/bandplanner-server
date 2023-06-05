from django.db import models



class SingleRelease(models.Model):

    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='singlereleases')
    song_title = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    upc = models.IntegerField(blank=True)
    isrc = models.IntegerField(blank=True)
    release_date = models.DateField()
    composer = models.CharField(max_length=50)
    producer = models.CharField(max_length=50)
    explicit = models.BooleanField()
    audio_url = models.URLField(max_length=200, blank=True)
    artwork =  models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    uploaded_to_distro = models.BooleanField()
