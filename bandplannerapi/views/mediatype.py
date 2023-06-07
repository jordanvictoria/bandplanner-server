"""View module for handling requests about media types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import MediaType


class MediaTypeView(ViewSet):
    """Bandplanner media type view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single media type

        Returns:
            Response -- JSON serialized media type
        """

        try:
            media_type = MediaType.objects.get(pk=pk)
            serializer = MediaTypeSerializer(media_type)
            return Response(serializer.data)
            
        except MediaType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all media types

        Returns:
            Response -- JSON serialized list of media types
        """

        media_types = MediaType.objects.all()
        serializer = MediaTypeSerializer(media_types, many=True)
        return Response(serializer.data)


class MediaTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for media types
    """
    class Meta:
        model = MediaType
        fields = ('id', 'label')
