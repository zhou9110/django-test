from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse


@api_view(['GET'])
def get_profile(request):
    if (not request.user.is_authenticated):
        return Response("USER IS NOT AUTHENTICATED", status=400)
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    serializer = ProfileSerializer(profile)
    return JsonResponse(serializer.data)

@api_view(['PUT'])
def edit_profile(request):
    if (not request.user.is_authenticated):
        return Response("USER IS NOT AUTHENTICATED", status=400)
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    data = request.data
    serializer = ProfileSerializer(profile, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=400)
