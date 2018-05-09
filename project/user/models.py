from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone


class Profile(models.Model):
    user = models.ForeignKey(
        User,
        models.CASCADE
    )
    MALE = 'M'
    FEMALE = 'F'
    NOT_SPECIFIED = 'NS'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NOT_SPECIFIED, 'Not Specified'),
    )
    mobile = models.CharField(max_length=32, null=True)
    bio = models.CharField(max_length=128, null=True)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        null=True,
    )
    profile_image = models.CharField(max_length=256, null=True)

class Follow(models.Model):
    following = models.ForeignKey(
        User,
        models.CASCADE,
        related_name="who_follows",
    )
    follower = models.ForeignKey(
        User,
        models.CASCADE,
        related_name="who_is_followed",
    )
    timestamp = models.DateTimeField(auto_now_add=True)
