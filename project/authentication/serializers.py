from rest_framework import serializers
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class UpdatePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
