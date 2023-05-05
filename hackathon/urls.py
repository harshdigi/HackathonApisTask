from django.urls import path, include
from rest_framework import routers
from .views import HackathonCreateAPIView, register_hackathon, HackathonSubmissionAPIView

router = routers.SimpleRouter()
router.register('hackathons', HackathonCreateAPIView, basename="hackathon")
router.register('submission', HackathonSubmissionAPIView, basename="submission")
urlpatterns = [
    path('', include(router.urls)),
    path('register_hackathon',view= register_hackathon, name= "register_hackathon")
]
