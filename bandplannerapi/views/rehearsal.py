from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import Rehearsal, Event, BandUser




class RehearsalView(ViewSet):
    """Rehearsal view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single rehearsals

        Returns:
            Response -- JSON serialized rehearsals
        """

        try:
            rehearsal = Rehearsal.objects.get(pk=pk)
            serializer = RehearsalSerializer(rehearsal)
            return Response(serializer.data)

        except Rehearsal.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all rehearsals

        Returns:
            Response -- JSON serialized list of rehearsals
        """

        rehearsals = Rehearsal.objects.filter(user=request.auth.user.id)
        serializer = RehearsalSerializer(rehearsals, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized rehearsal instance
        """
        current_user = BandUser.objects.get(user=request.auth.user)
        serializer = CreateRehearsalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a rehearsal

        Returns:
            Response -- Empty body with 204 status code
        """
    
        rehearsal = Rehearsal.objects.get(pk=pk)
        rehearsal.location = request.data["location"]
        rehearsal.band_info = request.data["band_info"]
        
        rehearsal_event = Event.objects.get(pk=request.data["event"])
        rehearsal.event = rehearsal_event

        user = BandUser.objects.get(pk=request.data["user"])
        rehearsal.user = user

        rehearsal.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a rehearsal"""
        
        rehearsal = Rehearsal.objects.get(pk=pk)
        rehearsal.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateRehearsalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rehearsal
        fields = ['id', 'user', 'event', 'location', 'band_info']



class EventSerializer(serializers.ModelSerializer):
    """For events."""
    class Meta:
        model = Event
        fields = ('id', 'user', 'event_type', 'title', 'date', 'time', 'description')

class UserSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = BandUser
        fields = ('id', 'user', 'project_title', 'bio', 'streaming', 'website', 'instagram', 'twitter', 'facebook', 'tiktok', 'full_name')



class RehearsalSerializer(serializers.ModelSerializer):
    """JSON serializer for rehearsals
    """
    event = EventSerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = Rehearsal
        fields = ('id', 'user', 'event', 'location', 'band_info')
        depth = 1
        