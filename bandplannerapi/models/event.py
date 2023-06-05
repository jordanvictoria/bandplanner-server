from django.db import models



class Event(models.Model):

    user = models.ForeignKey("BandUser", on_delete=models.CASCADE, related_name='events')
    event_type = models.ForeignKey("EventType", on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField(auto_now=False, auto_now_add=False)
    description = models.TextField(max_length=10000)
    
    