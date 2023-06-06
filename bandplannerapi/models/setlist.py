from django.db import models



class Setlist(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE, related_name='setlists')
    title = models.CharField(max_length=50)
    notes = models.TextField(max_length=500, blank=True)
    date_created = models.DateField()
    last_edited = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    
    