from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse


@api_view(['GET'])
def user_get_profile(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    # serialize data
    profile = Profile.objects.get(user_id=request.user.id)
    serializer = ProfileSerializer(profile)
    return JsonResponse(serializer.data)

@api_view(['PUT'])
def user_edit_profile(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    # serialize data
    profile = Profile.objects.get(user_id=request.user.id)
    data = request.data
    serializer = ProfileSerializer(profile, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
def user_follow(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    data = request.data
    try:
        data['username']
    except Exception as e:
        return JsonResponse({
                "command"   :   "FOLLOW_FAILED",
                "info"      :   str(e)
            }, status=400)
    follower = User.objects.get(username=data['username'])
    try:
        Follow.objects.get(following_id=request.user.id,follower_id=follower.id)
        return JsonResponse({
                "command"   :   "FOLLOW_FAILED",
                "info"      :   "follow state already exist"
            }, status=400)
    except Exception as _:
        follow = Follow(following_id=request.user.id,follower_id=follower.id)
        follow.save()
        return JsonResponse({
                "command"   :   "FOLLOW_SUCCESS"
            }, status=200)

@api_view(['POST'])
def user_unfollow(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    data = request.data
    try:
        data['username']
    except Exception as e:
        return JsonResponse({
                "command"   :   "UNFOLLOW_FAILED",
                "info"      :   str(e)
            }, status=400)
    follower = User.objects.get(username=data['username'])
    try:
        follow = Follow.objects.get(following_id=request.user.id,follower_id=follower.id)
        follow.delete()
        return JsonResponse({
                "command"   :   "UNFOLLOW_SUCCESS"
            }, status=200)
    except Exception as _:
        return JsonResponse({
                "command"   :   "UNFOLLOW_FAILED",
                "info"      :   "follow state does not exist"
            }, status=400)

@api_view(['GET'])
def user_get_following(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    query = Follow.objects.filter(following_id=request.user.id)
    response = []
    for follow in query:
        serializer = FollowSerializer(follow)
        response.append(serializer.data['follower'])
    return JsonResponse(response, safe=False, status=200)

@api_view(['GET'])
def user_get_followers(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    query = Follow.objects.filter(follower_id=request.user.id)
    response = []
    for follow in query:
        serializer = FollowSerializer(follow)
        response.append(serializer.data['following'])
    return JsonResponse(response, safe=False, status=200)
