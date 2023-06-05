from django.db import models



class MediaType(models.Model):

    label = models.CharField(max_length=50)
    
    