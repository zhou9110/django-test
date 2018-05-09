from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    recipient  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    timestamp = models.IntegerField()
    text = models.TextField()
    read = models.BooleanField(default=False)
