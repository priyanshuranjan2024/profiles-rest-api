from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status #contains http status codes
from rest_framework.authentication import TokenAuthentication # to authenticate the user
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated


from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions



class HelloApiView(APIView):
    """Test API View"""
    #creating the serializer_class attribute
    serializer_class = serializers.HelloSerializer
    #creating the get method
    def get(self,request,format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]
        #returning the response
        return Response({'message':'Hello!','an_apiview':an_apiview})
    
    def post(self, request):
        """Create a hello message with our name"""
        # Creating a serializer object
        serializer = self.serializer_class(data=request.data)
        # Checking if the serializer is valid
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'  # f-string to insert a variable in the string
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
            
    
    def put(self,request,pk=None):
        #pk is the primary key of the object to be updated since we are just testing we are not using it
        """Handle updating an object"""
        return Response({'method':'PUT'})
    
    def patch(self,request,pk=None):
        """Handle a partial update of an object"""
        return Response({'method':'PATCH'})
    
    
    def delete(self,request,pk=None):
        """Delete an object"""
        return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer
    
    def list(self,request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        return Response({'message':'Hello!','a_viewset':a_viewset})
    
    def create(self,request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def retrieve(self,request,pk=None): #pk is the primary key id
        """Handle getting an object by its ID"""
        return Response({'http_method':'GET'})
    
    def update(self,request,pk=None):
        """Handle updating an object"""
        return Response({'http_method':'PUT'})
    
    def partial_update(self,request,pk=None):
        """Handle updating part of an object"""
        return Response({'http_method':'PATCH'})
    
    def destroy(self,request,pk=None):
        """Handle removing an object"""
        return Response({'http_method':'DELETE'})
    

#creating a model viewset
class UserProfileViewSet(viewsets.ModelViewSet):
    """handle creating and updating profiles"""
    #now create the serializer class and then create the queryset so that we know 
    #what we are going to use in this viewset
    serializer_class=serializers.UserProfileSerializer
    queryset=models.UserProfile.objects.all()
    authentication_classes=(TokenAuthentication,)#this will be created as a tuple and will authenticate the users
    #if you want add more authentication techniques just add them in authetication class
    #now add the permission class
    permission_classes=(permissions.UpdateOwnProfile,)
    
    #adding the search functionality
    filter_backends=(filters.SearchFilter,)
    search_fields=('name','email',)#which fields are searchable
    
    
    
#creating the login api
class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    #this api is not visible by default so we have to overwrite the default functionality
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES
    #now add this to the urls.py file
    


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handle creating, reading and updating profile feed items"""
    authentication_classes=(TokenAuthentication,)
    #now call the serializer class
    serializer_class=serializers.ProfileFeedItemSerializer
    queryset=models.ProfileFeedItem.objects.all()
    permission_classes=(
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )
    
    #since we want to make the user_profile to come from the authentication 
    #we have to overwrite the default create functionality
    def perform_create(self,serializer):
        """Sets  the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)