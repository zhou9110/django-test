from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import permissions, viewsets
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializers import *
from rest_framework.views import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout, models
import json

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(['POST'])
def user_register(request):
    try:
        data = request.data
        user = User.objects.create_user(data['username'], data['email'], data['password'])
        user.save()
        return Response("REGISTER SUCCESS")
    except Exception as e:
        print(e)
        return Response("REGISTER FAILED", status=500)

@api_view(['POST'])
def user_login(request):
    try:
        data = request.data
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return Response("LOGIN SUCCESS") 
        else:
            # Return an 'invalid login' error message.
            return Response("LOGIN FAILED", status=500)
    except Exception as e:
        print(e)
        return Response("LOGIN FAILED", status=500) 

@api_view(['POST'])
def user_change_password(request):
    try:
        data = request.data
        username = data['username']
        password = data['password']
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return Response("CHANGE PASSWORD SUCCESS")
    except Exception as e:
        print(e)
        return Response("CHANGE PASSWORD FAILED", status=500)

@api_view(['GET'])
def user_logout(request):
    try:
        logout(request)
        return Response("LOGOUT SUCCESS")
    except Exception as e:
        print(e)
        return Response("LOGOUT FAILED", status=500)
