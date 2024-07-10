from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""
    
    def has_object_permission(self,request,view,obj):
        """checking if user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.id==request.user.id #this will check if the user is trying to edit their own profile
    
    
#permission for users to update their status
class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status only"""
    
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user_profile.id==request.user.id 