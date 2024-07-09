from django.urls import path
from profiles_api import views

#creating the url patterns
urlpatterns = [
    path('hello-view/',views.HelloApiView.as_view())
]


