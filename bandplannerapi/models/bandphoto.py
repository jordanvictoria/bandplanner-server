from django.db import models



class BandPhoto(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100)
    