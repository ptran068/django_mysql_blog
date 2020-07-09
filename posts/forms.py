from django import forms
from .models import Post, Profile, Comment

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address','Dob','image','cover_photos']



class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class videoform(forms.ModelForm):
    class Mete:
        model = Post
        fields = ('video', 'caption')