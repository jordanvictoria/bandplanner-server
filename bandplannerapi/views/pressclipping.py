from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import PressClipping, BandUser




class PressClippingView(ViewSet):
    """press clipping view"""

    def retrieve(self, request, pk):
        """Handle GET requests for press clippings

        Returns:
            Response -- JSON serialized press clippings
        """

        try:
            press_clipping = PressClipping.objects.get(pk=pk)
            serializer = PressClippingSerializer(press_clipping)
            return Response(serializer.data)

        except PressClipping.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all press clippings

        Returns:
            Response -- JSON serialized list of press clippings
        """

        press_clippings = PressClipping.objects.filter(user=request.auth.user.id)
        serializer = PressClippingSerializer(press_clippings, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized press clipping instance
        """
        
        current_user = BandUser.objects.get(user=request.auth.user)
        serializer = CreatePressClippingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a press clipping

        Returns:
            Response -- Empty body with 204 status code
        """

        press_clipping = PressClipping.objects.get(pk=pk)
        press_clipping.title = request.data["title"]
        press_clipping.date = request.data["date"]
        press_clipping.author = request.data["author"]
        press_clipping.description = request.data["description"]
        press_clipping.link = request.data["link"]

        user = BandUser.objects.get(pk=request.data["user"])
        press_clipping.user = user

        press_clipping.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for a press clipping"""
        
        press_clipping = PressClipping.objects.get(pk=pk)
        press_clipping.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreatePressClippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PressClipping
        fields = ['id', 'user', 'title', 'date', 'author', 'description', 'link']

class UserSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = BandUser
        fields = ('id', 'user', 'project_title', 'bio', 'streaming', 'website', 'instagram', 'twitter', 'facebook', 'tiktok', 'full_name', 'photo')


class PressClippingSerializer(serializers.ModelSerializer):
    """JSON serializer for press clipping
    """
    user = UserSerializer(many=False)

    class Meta:
        model = PressClipping
        fields = ('id', 'user', 'title', 'date', 'author', 'description', 'link')
        depth = 1
        