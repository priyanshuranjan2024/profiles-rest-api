from django.urls import path,include #importing the path function from django.urls
from profiles_api import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('hello-viewset',views.HelloViewSet,base_name='hello-viewset')

router.register('profile',views.UserProfileViewSet) #if you are giving the queryset then don't give the base_name as django will figure out the name on its own




#creating the url patterns
urlpatterns = [
    path('hello-view/',views.HelloApiView.as_view()),
    path('',include(router.urls)),#generates a set of urls for the ones that are registered in the router
    
    
] 


