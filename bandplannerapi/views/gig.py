from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import Gig, Event, BandUser




class GigView(ViewSet):
    """Gig view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single gigs

        Returns:
            Response -- JSON serialized gigs
        """

        try:
            gig = Gig.objects.get(pk=pk)
            serializer = GigSerializer(gig)
            return Response(serializer.data)

        except Gig.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all gigs

        Returns:
            Response -- JSON serialized list of gigs
        """

        gigs = Gig.objects.filter(user=request.auth.user.id)
        serializer = GigSerializer(gigs, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized gig instance
        """
        current_user = BandUser.objects.get(user=request.auth.user)
        serializer = CreateGigSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a gig

        Returns:
            Response -- Empty body with 204 status code
        """

        gig = Gig.objects.get(pk=pk)
        gig.city_state = request.data["city_state"]
        gig.venue = request.data["venue"]
        gig.band_info = request.data["band_info"]
        gig.age_requirement = request.data["age_requirement"]
        gig.ticket_price = request.data["ticket_price"]
        gig.ticket_link = request.data["ticket_link"]
        gig.guarantee = request.data["guarantee"]
        gig.sold_out = request.data["sold_out"]
        gig.announced = request.data["announced"]
        gig.flier = request.data["flier"]
        gig.stage_plot = request.data["stage_plot"]
        gig.input_list = request.data["input_list"]
        
        gig_event = Event.objects.get(pk=request.data["event"])
        gig.event = gig_event

        user = BandUser.objects.get(pk=request.data["user"])
        gig.user = user

        gig.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a gig"""
        
        gig = Gig.objects.get(pk=pk)
        gig.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateGigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gig
        fields = ['id', 'user', 'event', 'city_state', 'venue', 'band_info', 'age_requirement', 'ticket_price', 'ticket_link', 'guarantee', 'sold_out', 'announced', 'flier', 'stage_plot', 'input_list']



class EventSerializer(serializers.ModelSerializer):
    """For events."""
    class Meta:
        model = Event
        fields = ('id', 'user', 'event_type', 'title', 'date', 'time', 'description')

class UserSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = BandUser
        fields = ('id', 'user', 'project_title', 'bio', 'streaming', 'website', 'instagram', 'twitter', 'facebook', 'tiktok', 'full_name','photo')


class GigSerializer(serializers.ModelSerializer):
    """JSON serializer for gigs
    """
    event = EventSerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = Gig
        fields = ('id', 'user', 'event', 'city_state', 'venue', 'band_info', 'age_requirement', 'ticket_price', 'ticket_link', 'guarantee', 'sold_out', 'announced', 'flier', 'stage_plot', 'input_list')
        depth = 1
        