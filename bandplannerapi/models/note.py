from django.db import models



class Note(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=10000)
    date_created = models.DateField()
    last_edited = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    