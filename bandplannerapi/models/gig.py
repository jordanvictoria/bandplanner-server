from django.db import models



class Gig(models.Model):

    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='gigs')
    city_state = models.CharField(max_length=50)
    venue = models.CharField(max_length=50)
    band_info = models.TextField(max_length=500, blank=True)
    age_requirement = models.CharField(max_length=50, blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    ticket_link = models.URLField(max_length=200, blank=True)
    guarantee = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    sold_out = models.BooleanField(null=True)
    announced = models.BooleanField(null=True)
    flier = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, blank=True)
    stage_plot = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, blank=True)
    input_list = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, blank=True)
