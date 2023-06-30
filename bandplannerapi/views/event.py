from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import Event, EventType, BandUser




class EventView(ViewSet):
    """Event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single events

        Returns:
            Response -- JSON serialized events
        """

        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """

        events = Event.objects.filter(user=request.auth.user.id)


        e_type = request.query_params.get('event_type', None)
        if e_type is not None:
            type_object = EventType.objects.get(pk=e_type)
            events = events.filter(event_type = type_object)


        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized event instance
        """
        
        current_user = BandUser.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.title = request.data["title"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.description = request.data["description"]
        
        event_type = EventType.objects.get(pk=request.data["event_type"])
        event.event_type = event_type

        user = BandUser.objects.get(pk=request.data["user"])
        event.user = user

        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for an event"""
        
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'user', 'event_type', 'title', 'date', 'time', 'description']

class UserSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = BandUser
        fields = ('id', 'user', 'project_title', 'bio', 'streaming', 'website', 'instagram', 'twitter', 'facebook', 'tiktok', 'full_name', 'photo')

class EventTypeSerializer(serializers.ModelSerializer):
    """For event types."""
    class Meta:
        model = EventType
        fields = ('id', 'label')


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    user = UserSerializer(many=False)
    event_type = EventTypeSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'user', 'event_type', 'title', 'date', 'time', 'description')
        depth = 1
        