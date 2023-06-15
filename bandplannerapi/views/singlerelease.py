from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import SingleRelease, Event, BandUser





class SingleReleaseView(ViewSet):
    """Single Release view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single releases

        Returns:
            Response -- JSON serialized single releases
        """

        try:
            single_release = SingleRelease.objects.get(pk=pk)
            serializer = SingleReleaseSerializer(single_release)
            return Response(serializer.data)

        except SingleRelease.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all single releases

        Returns:
            Response -- JSON serialized list of single releases
        """

        single_releases = SingleRelease.objects.filter(user=request.auth.user.id)
        serializer = SingleReleaseSerializer(single_releases, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized single release instance
        """
        current_user = BandUser.objects.get(user=request.auth.user)
        serializer = CreateSingleReleaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a single release

        Returns:
            Response -- Empty body with 204 status code
        """

        single_release = SingleRelease.objects.get(pk=pk)
        single_release.song_title = request.data["song_title"]
        single_release.genre = request.data["genre"]
        single_release.upc = request.data["upc"]
        single_release.isrc = request.data["isrc"]
        single_release.composer = request.data["composer"]
        single_release.producer = request.data["producer"]
        single_release.explicit = request.data["explicit"]
        single_release.audio_url = request.data["audio_url"]
        single_release.artwork = request.data["artwork"]
        single_release.uploaded_to_distro = request.data["uploaded_to_distro"]
        
        single_event = Event.objects.get(pk=request.data["event"])
        single_release.event = single_event

        user = BandUser.objects.get(pk=request.data["user"])
        single_release.user = user

        single_release.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a single release"""
        
        single_release = SingleRelease.objects.get(pk=pk)
        single_release.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateSingleReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleRelease
        fields = ['id', 'user', 'event', 'song_title', 'genre', 'upc', 'isrc', 'composer', 'producer', 'explicit', 'audio_url', 'artwork', 'uploaded_to_distro']



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


class SingleReleaseSerializer(serializers.ModelSerializer):
    """JSON serializer for Single Releases
    """
    event = EventSerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = SingleRelease
        fields = ('id', 'user', 'event', 'song_title', 'genre', 'upc', 'isrc', 'composer', 'producer', 'explicit', 'audio_url', 'artwork', 'uploaded_to_distro')
        depth = 1
        