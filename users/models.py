from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.utils import timezone
from uuid import uuid4

class GenderChoices(models.TextChoices):
    male = "M", _("Male")
    female = "F", _("Female")
    other = "O", _("Other")
    no_preference = "NA", _("Prefer not to say")

class User(models.Model):
    user_id = models.UUIDField(
        primary_key=True, db_column="user_id", default=uuid.uuid4, editable=False
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null= True, blank=True)
    email = models.CharField(max_length=255, unique=True)
    password =models.CharField(max_length=255, editable=False)
    is_active = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar_url = models.URLField(default="")
    details = models.JSONField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GenderChoices.choices, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "users"
        verbose_name = "App User"
        verbose_name_plural = "App Users"

    def __str__(self):
        return "{email} - {first_name} {last_name}- ({user_id})".format(
            email=self.email,
            last_name=self.last_name,
            first_name = self.first_name,
            user_id=str(self.user_id),
        )
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        result = check_password(raw_password,self.password)
        print(result)
        return result
    




class AppUserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True, default=uuid4)
    created = models.DateTimeField(default=timezone.now)