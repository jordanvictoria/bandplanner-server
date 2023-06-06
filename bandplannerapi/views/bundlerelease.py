from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import BundleRelease, Event




class BundleReleaseView(ViewSet):
    """Bundle Release view"""

    def retrieve(self, request, pk):
        """Handle GET requests for bundle releases

        Returns:
            Response -- JSON serialized bundle releases
        """

        try:
            bundle_release = BundleRelease.objects.get(pk=pk)
            serializer = BundleReleaseSerializer(bundle_release)
            return Response(serializer.data)

        except BundleRelease.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all bundle releases

        Returns:
            Response -- JSON serialized list of bundle releases
        """

        bundle_releases = BundleRelease.objects.filter(user=request.auth.user.id)
        serializer = BundleReleaseSerializer(bundle_releases, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized bundle release instance
        """
        
        serializer = CreateBundleReleaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a bundle release

        Returns:
            Response -- Empty body with 204 status code
        """

        bundle_release = BundleRelease.objects.get(pk=pk)
        bundle_release.bundle_title = request.data["bundle_title"]
        bundle_release.genre = request.data["genre"]
        bundle_release.upc = request.data["upc"]
        bundle_release.audio_url = request.data["audio_url"]
        bundle_release.artwork = request.data["artwork"]
        bundle_release.uploaded_to_distro = request.data["uploaded_to_distro"]
        
        bundle_event = Event.objects.get(pk=request.data["event"])
        bundle_release.event = bundle_event

        bundle_release.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a bundle release"""
        
        bundle_release = BundleRelease.objects.get(pk=pk)
        bundle_release.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateBundleReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundleRelease
        fields = ['id', 'event', 'bundle_title', 'genre', 'upc', 'audio_url', 'artwork', 'uploaded_to_distro']



class EventSerializer(serializers.ModelSerializer):
    """For events."""
    class Meta:
        model = Event
        fields = ('id', 'user', 'event_type', 'title', 'date', 'time', 'description')


class BundleReleaseSerializer(serializers.ModelSerializer):
    """JSON serializer for bundle releases
    """
    event = EventSerializer(many=False)

    class Meta:
        model = BundleRelease
        fields = ('id', 'event', 'bundle_title', 'genre', 'upc', 'audio_url', 'artwork', 'uploaded_to_distro')
        depth = 1
        