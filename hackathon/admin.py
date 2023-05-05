from django.contrib import admin
from .models import Hackathon, HackathonRegistration,HackathonSubmission
# Register your models here.
admin.site.register(Hackathon)
admin.site.register(HackathonRegistration)
admin.site.register(HackathonSubmission)