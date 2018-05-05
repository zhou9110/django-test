from django.shortcuts import render
 
from rest_framework import viewsets
from rest_framework.views import Response
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def custom_view(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        return Response("Some Get Response")

    elif request.method == 'POST':
        data = request.data
        return Response("Some Post Response")
