from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

# Use this if
    # Your interface is not using standard CRUD operations
    # You're building something complex
    # You plan to customize the logic
    # You are not working with standard data structures

class TestApiView(APIView):
    # Test API View
    serializer_class = serializers.TestSerializer

    def get(self, request, format = None): # Get request to API
        # Returns a list of APIView features
        an_apiview = [
            'Using HTTP methods as functions (get, post, patch, put, delete)',
            'Similar to a traditional Django View',
            'Gives the most control over application logic',
            'Mapped manually to URLs',
        ]

        return Response({'message': 'Success!', 'an_apiview': an_apiview})

    def post(self, request): # Post request to API
        # Create a message with user name
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Thank you, {name}'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk = None):
        # Handle updating an object
        return Response({'method' : 'PUT'})

    def patch(self, request, pk = None):
        # Handle a partial update of an object
        return Response({'method' : 'PATCH'})

    def delete(self, request, pk = None):
        # Delete an object
        return Response({'method' : 'DELETE'})

# Use this instead of APIView when you
    # Are building a simple CRUD interface to the database
    # Are building a Quick and Simple API
    # Have little to no planned customization of logic
    # Are working with standard data structures

class TestViewSet(viewsets.ViewSet):
    # Test API ViewSet
    serializer_class = serializers.TestSerializer

    def list(self, request):
        # Return a test message
        a_viewset = [
            'Actions: (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using routers',
            'Typically provides more functionality with less code',
        ]
        return Response({'message': 'Welcome!', 'a_viewset': a_viewset})

    def create(self, request):
        # Create a new hello message
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Greetings, {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        # Handle getting an object by its ID
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        # Handle updating an object
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        # Handle updating part of an object
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        # Handle removing an object
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    # Handle creating and updating profiles
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    # Handle creating user authentication tokens
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    # Handles the creating, reading and updating of profile feed items
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        # Sets the user profile to the logged in user
        serializer.save(user_profile=self.request.user)
