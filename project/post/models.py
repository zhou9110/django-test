from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone

class Tag(models.Model):
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(Tag)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    images = models.TextField()
    location = models.TextField(null=True)

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
