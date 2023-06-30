from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import Song, BandUser




class SongView(ViewSet):
    """song view"""

    def retrieve(self, request, pk):
        """Handle GET requests for songs

        Returns:
            Response -- JSON serialized songs
        """

        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data)

        except Song.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all songs

        Returns:
            Response -- JSON serialized list of songs
        """

        songs = Song.objects.filter(user=request.auth.user.id)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized song instance
        """
        
        current_user = BandUser.objects.get(user=request.auth.user)
        serializer = CreateSongSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a song

        Returns:
            Response -- Empty body with 204 status code
        """

        song = Song.objects.get(pk=pk)
        song.name = request.data["name"]
        song.notes = request.data["notes"]

        user = BandUser.objects.get(pk=request.data["user"])
        song.user = user

        song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a song"""
        
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'user', 'name']

class UserSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = BandUser
        fields = ('id', 'user', 'project_title', 'bio', 'streaming', 'website', 'instagram', 'twitter', 'facebook', 'tiktok', 'full_name', 'photo')


class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for song
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Song
        fields = ('id', 'user', 'name')
        depth = 1