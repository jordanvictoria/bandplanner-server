from django.db import models



class Song(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE, related_name='songs')
    name = models.CharField(max_length=50)
    notes = models.TextField(max_length=500, blank=True)
    
