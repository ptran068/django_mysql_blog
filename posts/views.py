from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like
from django.utils import timezone
from .forms import UserUpdateForm, NewCommentForm, PostCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.http import require_http_methods
from django.contrib.auth import decorators
from django.views import View
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def base(request):
    return render(request,'base.html')
#*args and **kwargs giup chung ta co the truyen  bao nhieu tham so vao ham cung dc

@require_http_methods(['POST', 'GET'])
def createUser(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email existed")
                return redirect('register')
            else:    
                user = User.objects.create_user(password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save();
                return redirect('login')

        else:
            messages.info(request, "password not matching")
            return redirect('register')

    else:
        return render(request, 'pages/createUser.html')


# @decorators.login_required(login_url='login')
def index(request):
    posts = Post.objects.all().filter(created_date__lte=timezone.now()).order_by('-created_date')
    user =request.user
    context={
        'posts' : posts,
        'user' : user,
    }
    return render(request,'index.html',context)

############################
#create Post
#authorize request.user.has_perm('posts.add_post')
class CreatePost(LoginRequiredMixin, CreateView):
    login_url ='/login'
    model = Post
    template_name = 'post_form.html'
    fields = ['image','caption']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetail(ListView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context[""] = 
        return context
    
