from django.shortcuts import render
from .models import Post
from django.views.generic import ListView

# Create your views here.
class ListPostView(ListView):
    
    def get (self, request, *args, **kwargs):
        template_name = 'blog/blog.html'
        obj = {
        'posts': Post.objects.all().order_by('-createdAt')
        }
        return render(request, template_name, obj)

#*args and **kwargs giup chung ta co the truyen  bao nhieu tham so vao ham cung dc