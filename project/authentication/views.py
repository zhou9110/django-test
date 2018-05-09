from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import permissions, viewsets
# from django.contrib import admin
# admin.autodiscover()
# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout, models
from django.http import HttpResponse, JsonResponse
from .serializers import *
from project.user.models import *
import json


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# /auth/register/
@api_view(['POST'])
def auth_register(request):
    # check authenticated
    # if (request.user.is_authenticated):
    #     return JsonResponse({
    #             "command"   :   "IS_AUTHENTICATED",
    #             "info"      :   "user is logged in"
    #         }, status=400)
    try:
        # get data
        data = request.data
        # create user
        user = User.objects.create_user(
                data['username'], 
                data['email'], 
                data['password']
            )
        user.save()
        # create profile
        profile = Profile.objects.create(user=user)
        profile.save()
        return JsonResponse({
                "command"   :   "REGISTER_SUCCESS", 
                "username"  :   data['username']
            }, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "REGISTER_FAILED",
                "info"      :   str(e)
            }, status=400)

# /auth/login/
@api_view(['POST'])
def auth_login(request):
    # check authenticated
    if (request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "LOGIN_FAILED",
                "info"      :   "user already logged in"
            }, status=400)
    try:
        # get data
        data = request.data
        user = None
        if ('username' in data):
            user = User.objects.get(username=data['username'])
        elif ('email' in data):
            user = User.objects.get(email=data['email'])
        # authenticate user
        user = authenticate(
                request, 
                username=user.username, 
                password=data['password']
            )
        if user is not None:
            # log user in
            login(request, user)
            return JsonResponse({
                    "command"   :   "LOGIN_SUCCESS", 
                    "username"  :   user.username
                }, status=200)
        else:
            # invalid login
            return JsonResponse({
                    "command"   :   "LOGIN_FAILED", 
                    "username"  :   user.username
                }, status=400)
    except Exception as e:
        return JsonResponse({
                "command"   :   "LOGIN_FAILED",
                "info"      :   str(e)
            }, status=400)

# /auth/update_password/
@api_view(['PUT'])
def auth_update_password(request):
    # check authenticated
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        # get data
        data = request.data
        # get user and update password
        user = User.objects.get(pk=request.user.id)
        user.set_password(data['password'])
        user.save()
        return JsonResponse({
                "command"   :   "UPDATE_PASSWORD_SUCCESS"
            }, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "UPDATE_PASSWORD_FAILED",
                "info"      :   str(e)
            }, status=400)

# /auth/logout/
@api_view(['GET'])
def auth_logout(request):
    # check authenticated
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
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
