from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import BandPhoto, BandUser




class BandPhotoView(ViewSet):
    """Event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single band photos

        Returns:
            Response -- JSON serialized band photos
        """

        try:
            band_photo = BandPhoto.objects.get(pk=pk)
            serializer = BandPhotoSerializer(band_photo)
            return Response(serializer.data)

        except BandPhoto.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all band photos

        Returns:
            Response -- JSON serialized list of band photos
        """

        band_photos = BandPhoto.objects.filter(user=request.auth.user.id)
        serializer = BandPhotoSerializer(band_photos, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized band_photo instance
        """
        
        current_user = BandUser.objects.get(user=request.auth.user)
        serializer = CreateBandPhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """Handle PUT requests for a band photo"""
        
        band_photo = BandPhoto.objects.get(pk=pk)
        band_photo.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateBandPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandPhoto
        fields = ['id', 'user', 'photo']

class UserSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = BandUser
        fields = ('id', 'user', 'project_title', 'bio', 'streaming', 'website', 'instagram', 'twitter', 'facebook', 'tiktok' 'full_name')


class BandPhotoSerializer(serializers.ModelSerializer):
    """JSON serializer for band photos
    """
    user = UserSerializer(many=False)

    class Meta:
        model = BandPhoto
        fields = ('id', 'user', 'photo')
        depth = 1
        