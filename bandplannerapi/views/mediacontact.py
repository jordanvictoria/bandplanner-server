from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bandplannerapi.models import MediaContact, BandUser, MediaType




class MediaContactView(ViewSet):
    """Media contact view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single media contact

        Returns:
            Response -- JSON serialized media contact
        """

        try:
            event = MediaContact.objects.get(pk=pk)
            serializer = MediaContactSerializer(event)
            return Response(serializer.data)

        except MediaContact.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all media contacts

        Returns:
            Response -- JSON serialized list of media contacts
        """

        media_contacts = MediaContact.objects.filter(user=request.auth.user.id)

        m_type = request.query_params.get('media_type', None)
        if m_type is not None:
            type_object = MediaType.objects.get(pk=m_type)
            media_contacts = media_contacts.filter(media_type = type_object)

        serializer = MediaContactSerializer(media_contacts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized media contact instance
        """
        
        current_user = BandUser.objects.get(user=request.auth.user)
        serializer = CreateMediaContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a media contact

        Returns:
            Response -- Empty body with 204 status code
        """

        media_contact = MediaContact.objects.get(pk=pk)
        media_contact.organization = request.data["organization"]
        media_contact.contact = request.data["contact"]
        media_contact.role = request.data["role"]
        media_contact.location = request.data["location"]
        media_contact.email = request.data["email"]
        media_contact.website = request.data["website"]
        media_contact.notes = request.data["notes"]
        
        media_type = MediaType.objects.get(pk=request.data["media_type"])
        media_contact.media_type = media_type

        user = BandUser.objects.get(pk=request.data["user"])
        media_contact.user = user

        media_contact.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle PUT requests for an media contact"""
        
        media_contact = MediaContact.objects.get(pk=pk)
        media_contact.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)




class CreateMediaContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContact
        fields = ['id', 'user', 'media_type', 'organization', 'contact', 'role', 'location', 'email', 'website', 'notes', 'media_type']

class UserSerializer(serializers.ModelSerializer):
    """For users."""
    class Meta:
        model = BandUser
        fields = ('id', 'user', 'project_title', 'bio', 'streaming', 'website', 'instagram', 'twitter', 'facebook', 'tiktok', 'full_name', 'photo')

class MediaTypeSerializer(serializers.ModelSerializer):
    """For event types."""
    class Meta:
        model = MediaType
        fields = ('id', 'label')


class MediaContactSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    user = UserSerializer(many=False)
    media_type = MediaTypeSerializer(many=False)

    class Meta:
        model = MediaContact
        fields = ('id', 'user', 'media_type', 'organization', 'contact', 'role', 'location', 'email', 'website', 'notes', 'media_type')
        depth = 1