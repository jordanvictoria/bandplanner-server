from django.db import models


class SetlistSong(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE)
    setlist = models.ForeignKey("Setlist", on_delete=models.CASCADE, related_name='setlists')
    song = models.ForeignKey("Song", on_delete=models.CASCADE, related_name='songs')
    notes = models.TextField(max_length=500, blank=True)
    