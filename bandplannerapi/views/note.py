from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import Note, BandUser




class NoteView(ViewSet):
    """Note view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single notes

        Returns:
            Response -- JSON serialized notes
        """

        try:
            note = Note.objects.get(pk=pk)
            serializer = NoteSerializer(note)
            return Response(serializer.data)

        except Note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all notes

        Returns:
            Response -- JSON serialized list of notes
        """

        notes = Note.objects.filter(user=request.auth.user.id)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized note instance
        """
        
        current_user = BandUser.objects.get(user=request.auth.user)
        serializer = CreateNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a note

        Returns:
            Response -- Empty body with 204 status code
        """

        note = Note.objects.get(pk=pk)
        note.title = request.data["title"]
        note.content = request.data["content"]
        note.date_created = request.data["date_created"]
        note.last_edited = request.data["last_edited"]

        user = BandUser.objects.get(pk=request.data["user"])
        note.user = user

        note.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a note"""
        
        note = Note.objects.get(pk=pk)
        note.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'content', 'date_created', 'last_edited']

class UserSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = BandUser
        fields = ('id', 'user', 'project_title', 'bio', 'streaming', 'website', 'instagram', 'twitter', 'facebook', 'tiktok' 'full_name')


class NoteSerializer(serializers.ModelSerializer):
    """JSON serializer for note
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Note
        fields = ('id', 'user', 'title', 'content', 'date_created', 'last_edited')
        depth = 1
        