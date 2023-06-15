from django.db import models



class Gig(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE, related_name='gigs')
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='gigs')
    city_state = models.CharField(max_length=50)
    venue = models.CharField(max_length=50)
    band_info = models.TextField(max_length=500, blank=True)
    age_requirement = models.CharField(max_length=50, blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    ticket_link = models.URLField(max_length=200, blank=True)
    guarantee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sold_out = models.BooleanField(default=False)
    announced = models.BooleanField(default=False)
    flier = models.CharField(max_length=255, blank=True)
    stage_plot = models.CharField(max_length=255, blank=True)
    input_list = models.CharField(max_length=255, blank=True)
