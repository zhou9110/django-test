from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse


# /user/profile/
@api_view(['GET'])
def user_profile(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        profile = Profile.objects.get(user_id=request.user.id)
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_PROFILE_FAILED",
                "info"      :   str(e)
            }, status=400)

# /user/profile/<id>/
@api_view(['GET'])
def user_profile_by_id(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        profile = Profile.objects.get(user_id=pk)
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_PROFILE_FAILED",
                "info"      :   str(e)
            }, status=400)

# /user/update_profile/
@api_view(['PUT'])
def user_update_profile(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        profile = Profile.objects.get(user_id=request.user.id)
        data = request.data
        data['user'] = request.user.id
        serializer = ProfileSerializer(profile, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        return JsonResponse({
                "command"   :   "UPDATE_PROFILE_FAILED",
                "info"      :   str(e)
            }, status=400)

# /user/follow/<id>/
@api_view(['POST'])
def user_follow(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        follower = User.objects.get(pk=pk)
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
    except Exception as e:
        return JsonResponse({
                "command"   :   "FOLLOW_FAILED",
                "info"      :   str(e)
            }, status=400)

# /user/unfollow/<id>/
@api_view(['POST'])
def user_unfollow(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        follower = User.objects.get(pk=pk)
        follow = Follow.objects.get(following_id=request.user.id,follower_id=follower.id)
        follow.delete()
        return JsonResponse({
                "command"   :   "UNFOLLOW_SUCCESS"
            }, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "UNFOLLOW_FAILED",
                "info"      :   str(e)
            }, status=400)

# /user/following/
@api_view(['GET'])
def user_following(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        query = Follow.objects.filter(following_id=request.user.id)
        response = []
        for follow in query:
            serializer = FollowSerializer(follow)
            response.append(serializer.data['follower'])
        return JsonResponse(response, safe=False, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_FOLLOWING_FAILED",
                "info"      :   str(e)
            }, status=400)

# /user/following/<id>/
@api_view(['GET'])
def user_following_by_id(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        query = Follow.objects.filter(following_id=pk)
        response = []
        for follow in query:
            serializer = FollowSerializer(follow)
            response.append(serializer.data['follower'])
        return JsonResponse(response, safe=False, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_FOLLOWING_FAILED",
                "info"      :   str(e)
            }, status=400)

# /user/followers/
@api_view(['GET'])
def user_followers(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        query = Follow.objects.filter(follower_id=request.user.id)
        response = []
        for follow in query:
            serializer = FollowSerializer(follow)
            response.append(serializer.data['following'])
        return JsonResponse(response, safe=False, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_FOLLOWERS_FAILED",
                "info"      :   str(e)
            }, status=400)

# /user/followers/<id>/
@api_view(['GET'])
def user_followers_by_id(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        query = Follow.objects.filter(follower_id=pk)
        response = []
        for follow in query:
            serializer = FollowSerializer(follow)
            response.append(serializer.data['following'])
        return JsonResponse(response, safe=False, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_FOLLOWERS_FAILED",
                "info"      :   str(e)
            }, status=400)
