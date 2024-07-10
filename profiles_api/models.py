from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


#Create the custom user manager so that we can create users using the user model that we created
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    #make a function to create a user
    def create_user(self,email,name,password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')
        #normalize the email address
        email=self.normalize_email(email)
        user=self.model(email=email,name=name)

        #set the password and this will be hashed   
        user.set_password(password)
        #save the user
        user.save(using=self._db)

        return user
    
    #now we will create the superuser and password is required
    def create_superuser(self,email,name,password):
        """Create and save a new superuser with given details"""
        user=self.create_user(email,name,password)

        user.is_superuser=True
        user.is_staff=True

        user.save(using=self._db)

        return user



class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Database model for users in the system"""
    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False) # is_staff if true gives access do django admin

    #now we need to create a user manager class custom
    objects=UserProfileManager() 

    #since we are overriding the default username field we need to specify the USERNAME_FIELD
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name
    
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name
    
    def __str__(self):
        """Return string representation of our user"""
        return self.email
    
    
#model for the user profile feed
class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile=models.ForeignKey(
        #attach it with the auth model so that it can switch the model if we change it
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE #if the associated user profile is deleted then delete the attached feed
    )
    
    status_text=models.CharField(max_length=255)
    created_on=models.DateTimeField(auto_now_add=True)
    
    #for displaying convert this object into string and display the status_text
    def __str__(self):
        """Return the model as a string"""
        return self.status_text