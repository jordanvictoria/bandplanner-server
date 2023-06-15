from django.db import models



class Rehearsal(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE, related_name='rehearsals')
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='rehearsals')
    location = models.CharField(max_length=50)
    band_info = models.TextField(max_length=500, blank=True)

