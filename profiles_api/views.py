from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #contains http status codes
from profiles_api import serializers


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
