from django.urls import path, include
from rest_framework import routers
from .views import HackathonCreateAPIView, register_hackathon, HackathonSubmissionAPIView,HackathonUser

router = routers.SimpleRouter()
router.register('hackathons', HackathonCreateAPIView, basename="hackathon")
router.register('submission', HackathonSubmissionAPIView, basename="submission")
router.register('registered_user', HackathonUser, basename="registered_users" )
urlpatterns = [
    path('', include(router.urls)),
    path('register_hackathon',view= register_hackathon, name= "register_hackathon")
]
