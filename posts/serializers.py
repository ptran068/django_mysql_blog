from rest_framework import serializers
from .models import Post
from users.models import CustomUser
from django.contrib import messages
# from django.contrib.auth.models import auth
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from rest_framework.authentication import authenticate
#serializers lay du lieu tu moddel chuyen ve json cho client va nguowc lai

class GetAllPost(serializers.ModelSerializer):
    # author = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.get())
    class Meta:
        model = Post
        fields = ('id', 'caption', 'author')

    
class CreatePost(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('caption', 'image')

#auth
class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)
    password = serializers.CharField(max_length = 255)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Check if user sent email
           user = authenticate(email=email,password=password)
           if user is None:
               msg = ('Invalid email or password')
               raise exceptions.AuthenticationFailed(msg)
        else:
            raise exceptions.ValidationError('Emal and Password are required')
        attrs['user'] = user
        return attrs


class CreateComment(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('content')