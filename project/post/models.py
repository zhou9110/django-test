from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone


class Post(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        null=True
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    images = models.TextField()

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        null=True
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
