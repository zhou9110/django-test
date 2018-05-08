from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import permissions, viewsets
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout, models
from django.http import HttpResponse, JsonResponse
from .serializers import *
from project.user.models import *
import json


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
def auth_register(request):
    try:
        # serialize data
        data = request.data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid()
        # create user
        user = User.objects.create_user(
                serializer.data['username'], 
                serializer.data['email'], 
                serializer.data['password']
            )
        user.save()
        # create profile
        profile = Profile.objects.create(user=user)
        profile.save()
        return JsonResponse({
                "command"   :   "REGISTER_SUCCESS", 
                "username"  :   serializer.data['username']
            }, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "REGISTER_FAILED",
                "info"      :   str(e)
            }, status=400)

@api_view(['POST'])
def auth_login(request):
    try:
        # check authenticated
        if (request.user.is_authenticated):
            return JsonResponse({
                    "command"   :   "LOGIN_FAILED",
                    "info"      :   "user already logged in"
                }, status=400)
        # serialize data
        data = request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid()
        # authenticate user
        user = authenticate(
                request, 
                username=serializer.data['username'], 
                password=serializer.data['password']
            )
        if user is not None:
            # log user in
            login(request, user)
            return JsonResponse({
                    "command"   :   "LOGIN_SUCCESS", 
                    "username"  :   serializer.data['username']
                }, status=200)
        else:
            # invalid login
            return JsonResponse({
                    "command"   :   "LOGIN_FAILED", 
                    "username"  :   serializer.data['username']
                }, status=400)
    except Exception as e:
        return JsonResponse({
                "command"   :   "LOGIN_FAILED",
                "info"      :   str(e)
            }, status=400)

@api_view(['PUT'])
def auth_update_password(request):
    try:
        if (not request.user.is_authenticated):
            return JsonResponse({
                    "command"   :   "NOT_AUTHENTICATED",
                    "info"      :   "user is not authenticated"
                }, status=400)
        # serialize data
        data = request.data
        serializer = UpdatePasswordSerializer(data=data)
        serializer.is_valid()
        # get user and update password
        user = User.objects.get(pk=request.user.id)
        user.set_password(serializer.data['password'])
        user.save()
        return JsonResponse({
                "command"   :   "UPDATE_PASSWORD_SUCCESS"
            }, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "UPDATE_PASSWORD_FAILED",
                "info"      :   str(e)
            }, status=400)

@api_view(['GET'])
def auth_logout(request):
    try:
        if (not request.user.is_authenticated):
            return JsonResponse({
                    "command"   :   "NOT_AUTHENTICATED",
                    "info"      :   "user is not authenticated"
                }, status=400)
        # log user out
        logout(request)
        return JsonResponse({
                "command"   :   "LOGOUT_SUCCESS"
            }, status=200)
    except Exception as e:
        JsonResponse({
                "command"   :   "LOGOUT_FAILED",
                "info"      :   str(e)
            }, status=400)
