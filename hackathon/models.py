from django.db import models
from django.forms import ValidationError
from users.models import User
# Create your models here.

#Hackathon Model
class Hackathon(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(null= True, blank= True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_hackathons')   
    background_image = models.ImageField(upload_to='upload/hackathon_images/')
    hackathon_image = models.ImageField(upload_to='upload/hackathon_images/')
    TYPE_CHOICES = (
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'Link'),
    )
    submission_type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reward_prize = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title + " - " + self.created_by.email

#Registration Model
class HackathonRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registered_hackathons')
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hackathon.title + " - " + self.user.email

#Submission Model
class HackathonSubmission(models.Model):
    registration = models.ForeignKey(HackathonRegistration,on_delete = models.CASCADE, related_name="hackathon_submission")
    name = models.CharField(max_length=256)
    summary = models.TextField()
    submission_file = models.FileField(upload_to='upload/submission_files/', blank=True, null=True)
    submission_link = models.URLField(blank=True, null=True)
    submission_image = models.ImageField(upload_to='upload/submission_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.registration.user.email
    
    def clean(self):
        super().clean()
        if not self.submission_file and not self.submission_link and not self.submission_image:
            raise ValidationError("At least one of 'submission_file', 'submission_link', or 'submission_image' must be provided.")
