"""View module for handling requests about bandusers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import BandUser


class BandUserView(ViewSet):
    """Banduser view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single banduser

        Returns:
            Response -- JSON serialized banduser
        """

        try:
            band_user = BandUser.objects.get(pk=pk)
            serializer = BandUserSerializer(band_user)
            return Response(serializer.data)
        except BandUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all band users

        Returns:
            Response -- JSON serialized list of band users
        """

        band_users = BandUser.objects.all()
        serializer = BandUserSerializer(band_users, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a band user

        Returns:
            Response -- Empty body with 204 status code
        """

        band_user = BandUser.objects.get(pk=pk)
        band_user.project_title = request.data["project_title"]
        band_user.bio = request.data["bio"]
        band_user.streaming = request.data["streaming"]
        band_user.website = request.data["website"]
        band_user.instagram = request.data["instagram"]
        band_user.twitter = request.data["twitter"]
        band_user.facebook = request.data["facebook"]
        band_user.tiktok = request.data["tiktok"]

        band_user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class BandUserSerializer(serializers.ModelSerializer):
    """JSON serializer for band users
    """
    class Meta:
        model = BandUser
        fields = ('id', 'user', 'project_title', 'bio', 'streaming', 'website', 'instagram', 'twitter', 'facebook', 'tiktok' 'full_name')