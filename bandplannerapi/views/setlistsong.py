from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import SetlistSong, BandUser, Setlist, Song




class SetlistSongView(ViewSet):
    """SetlistSong view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single setlist songs

        Returns:
            Response -- JSON serialized setlist songs
        """

        try:
            setlist_song = SetlistSong.objects.get(pk=pk)
            serializer = SetlistSongSerializer(setlist_song)
            return Response(serializer.data)

        except SetlistSong.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all setlist songs

        Returns:
            Response -- JSON serialized list of setlist songs
        """

        setlist_songs = SetlistSong.objects.filter(user=request.auth.user.id)
        serializer = SetlistSongSerializer(setlist_songs, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized setlist song instance
        """
        
        user = BandUser.objects.get(user=request.auth.user.id)

        serializer = CreateSetlistSongSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a setlist song

        Returns:
            Response -- Empty body with 204 status code
        """

        setlist_song = SetlistSong.objects.get(pk=pk)
        setlist_song.notes = request.data["notes"]

        setlist = Setlist.objects.get(pk=request.data["setlist"])
        setlist_song.setlist = setlist

        song = Song.objects.get(pk=request.data["song"])
        setlist_song.song = song

        user = BandUser.objects.get(pk=request.data["user"])
        setlist_song.user = user
        
        setlist_song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a setlist song"""
        
        setlist_song = SetlistSong.objects.get(pk=pk)
        setlist_song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



class CreateSetlistSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetlistSong
        fields = ['id', 'setlist', 'song', 'notes']


class SetlistSerializer(serializers.ModelSerializer):
    """For setlists."""
    class Meta:
        model = Setlist
        fields = ('id', 'user', 'title', 'notes', 'date_created', 'last_edited')
        depth = 1

class SongSerializer(serializers.ModelSerializer):
    """For songs."""
    class Meta:
        model = Song
        fields = ('id', 'user', 'name')

class UserSetlistSongSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = BandUser
        fields = ('id', 'user', 'project_title', 'bio', 'streaming', 'website', 'instagram', 'twitter', 'facebook', 'tiktok', 'full_name')




class SetlistSongSerializer(serializers.ModelSerializer):
    """JSON serializer for setlist songs
    """
    setlist = SetlistSerializer(many=False)
    song = SongSerializer(many=False)
    user = UserSetlistSongSerializer(many=False)

    class Meta:
        model = SetlistSong
        fields = ('id', 'setlist', 'song', 'notes')
        depth = 2