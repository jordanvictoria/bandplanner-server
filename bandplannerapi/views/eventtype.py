"""View module for handling requests about event types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import EventType


class EventTypeView(ViewSet):
    """Bandplanner event type view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event type

        Returns:
            Response -- JSON serialized event type
        """

        try:
            event_type = EventType.objects.get(pk=pk)
            serializer = EventTypeSerializer(event_type)
            return Response(serializer.data)
        except EventType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all event types

        Returns:
            Response -- JSON serialized list of event types
        """

        event_types = EventType.objects.all()
        serializer = EventTypeSerializer(event_types, many=True)
        return Response(serializer.data)


class EventTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for event types
    """
    class Meta:
        model = EventType
        fields = ('id', 'label')