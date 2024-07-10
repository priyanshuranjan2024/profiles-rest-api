from rest_framework import serializers
from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=20)
    
    
#a model serializer

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    #we have to make a meta class so that this serializer interacts with a particular model
    class Meta:
        model=models.UserProfile
        #we have to create a list of all the fields that we want to make accesible
        fields=('id','email','name','password')
        #to make the password not available in the get we will add this functionality in
        #extra keyword args
        extra_kwargs={
            'password':{
                'write_only':True,
                'style':{'input_type':'password'},
            }
        }
    
    #overwrite the default create function to hash the password
    def create(self,validated_data): 
        """Create and return a new user"""
        user=models.UserProfile.objects.create_user( #this will call the userprofilemanager object
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        
        return user
    
    
#profile feed serializer
class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializers profile feed items"""
    class Meta:
        model=models.ProfileFeedItem
        fields=('id', 'user_profile','status_text','created_on')
        #make the user_profile read only so that it is only for the authenticated user
        extra_kwargs={'user_profile':{'read_only':True}}
    
        
    