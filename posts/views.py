from django.shortcuts import render
from .models import Post
from django.views.generic import ListView
from django.utils import timezone

# # Create your views here.
# class ListPostView(ListView):
    
#     def get (self, request, *args, **kwargs):
#         template_name = 'blog/blog.html'
#         obj = {
#         'posts': Post.objects.all().order_by('-createdAt')
#         }
#         return render(request, template_name, obj)

#*args and **kwargs giup chung ta co the truyen  bao nhieu tham so vao ham cung dc

def index(request):
    posts = Post.objects.all().filter(created_date__lte=timezone.now()).order_by('-created_date')
    user =request.user
    context={
        'posts' : posts,
        'user' : user,
    }
    return render(request,'index.html',context)

############################
# profile posts
def profile_posts(request):
    user = request.user
    
    posts = Post.objects.filter(author=request.user).order_by('-created_date')
    return render(request,'profile_posts.html',{'posts':posts, 'user':user})