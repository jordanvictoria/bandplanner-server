from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import BundleSong, BundleRelease




class BundleSongView(ViewSet):
    """Bundle song view"""

    def retrieve(self, request, pk):
        """Handle GET requests for bundle songs

        Returns:
            Response -- JSON serialized bundle songs
        """

        try:
            bundle_song = BundleSong.objects.get(pk=pk)
            serializer = BundleSongSerializer(bundle_song)
            return Response(serializer.data)

        except BundleSong.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all bundle songs

        Returns:
            Response -- JSON serialized list of bundle songs
        """

        bundle_songs = BundleSong.objects.filter(user=request.auth.user.id)
        serializer = BundleSongSerializer(bundle_songs, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized bundle song instance
        """
        
        serializer = CreateBundleSongSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a bundle song

        Returns:
            Response -- Empty body with 204 status code
        """

        bundle_song = BundleSong.objects.get(pk=pk)
        bundle_song.song_title = request.data["song_title"]
        bundle_song.genre = request.data["genre"]
        bundle_song.isrc = request.data["isrc"]
        bundle_song.composer = request.data["composer"]
        bundle_song.producer = request.data["producer"]
        bundle_song.explicit = request.data["explicit"]
        
        bundle = BundleRelease.objects.get(pk=request.data["bundle"])
        bundle_song.bundle = bundle

        bundle_song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a bundle song"""
        
        bundle_song = BundleSong.objects.get(pk=pk)
        bundle_song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateBundleSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundleSong
        fields = ['id', 'bundle', 'song_title', 'genre', 'isrc', 'composer', 'producer', 'explicit']



class BundleReleaseSerializer(serializers.ModelSerializer):
    """For Bundle releases."""
    class Meta:
        model = BundleRelease
        fields = ('id', 'event', 'bundle_title', 'genre', 'upc', 'audio_url', 'artwork', 'uploaded_to_distro')


class BundleSongSerializer(serializers.ModelSerializer):
    """JSON serializer for bundle songs
    """
    bundle = BundleReleaseSerializer(many=False)

    class Meta:
        model = BundleSong
        fields = ('id', 'bundle', 'song_title', 'genre', 'isrc', 'composer', 'producer', 'explicit')
        depth = 1
        