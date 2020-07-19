from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['address','image','cover_photos']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['email']

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class videoform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('video', 'caption')

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image', 'author']