from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import Setlist, BandUser




class SetlistView(ViewSet):
    """setlist view"""

    def retrieve(self, request, pk):
        """Handle GET requests for setlists

        Returns:
            Response -- JSON serialized setlist
        """

        try:
            setlist = Setlist.objects.get(pk=pk)
            serializer = SetlistSerializer(setlist)
            return Response(serializer.data)

        except Setlist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all setlists

        Returns:
            Response -- JSON serialized list of setlists
        """

        setlists = Setlist.objects.filter(user=request.auth.user.id)
        serializer = SetlistSerializer(setlists, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized setlist instance
        """
        
        current_user = BandUser.objects.get(user=request.auth.user)
        serializer = CreateSetlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a setlist

        Returns:
            Response -- Empty body with 204 status code
        """

        setlist = Setlist.objects.get(pk=pk)
        setlist.title = request.data["title"]
        setlist.notes = request.data["notes"]
        setlist.date_created = request.data["date_created"]
        setlist.last_edited = request.data["last_edited"]

        user = BandUser.objects.get(pk=request.data["user"])
        setlist.user = user

        setlist.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a setlist"""
        
        setlist = Setlist.objects.get(pk=pk)
        setlist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateSetlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setlist
        fields = ['id', 'user', 'title', 'notes', 'date_created', 'last_edited']

class UserSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = BandUser
        fields = ('id', 'user', 'project_title', 'bio', 'streaming', 'website', 'instagram', 'twitter', 'facebook', 'tiktok', 'full_name', 'photo')


class SetlistSerializer(serializers.ModelSerializer):
    """JSON serializer for setlist
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Setlist
        fields = ('id', 'user', 'title', 'notes', 'date_created', 'last_edited')
        depth = 1
        