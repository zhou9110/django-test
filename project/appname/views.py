from django.shortcuts import render
 
from rest_framework import viewsets
from .models import University, Student
from .serializers import UniversitySerializer, StudentSerializer
from rest_framework.views import APIView, Response
from rest_framework.decorators import api_view

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
 
class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

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
