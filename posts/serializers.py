from rest_framework import serializers
from .models import Post, Comment, Like
from users.models import CustomUser
from django.contrib import messages
# from django.contrib.auth.models import auth
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from rest_framework.authentication import authenticate
from users.models import CustomUser
# from django.contrib.auth import get_user_model

#serializers lay du lieu tu moddel chuyen ve json cho client va nguowc lai


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']
class GetAllPost(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(many=False, queryset=CustomUser.objects.get(id =author))
    author = UserSerializer(many=False)
    class Meta:
        model = Post
        fields = ('id', 'caption', 'author', 'image')

    
class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('caption', 'image')


class LikePostSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['value']


class CreateComment(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
        