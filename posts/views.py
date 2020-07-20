from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like
from django.utils import timezone
from .forms import UserUpdateForm, NewCommentForm, PostCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.contrib.auth import decorators
from django.contrib.auth import get_user_model
from django.db.models import Q


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.views import APIView 

#rest_apis
from rest_framework.response import Response
from rest_framework import status
from .serializers import GetAllPost, CreatePostSerializer, CreateComment, LikePostSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django_mysql.middlewares.authentication import AuthenticationJWT, SessionAuthentication
#ObtainAuthToken to custom view response

User = get_user_model()


@api_view(['GET', 'POST'])
@authentication_classes([AuthenticationJWT])
@permission_classes([IsAuthenticated])
def createCommentByApis(request, postID):
    if request.method == 'POST':
        
        serializers_comment = CreateComment(data = request.data)
        post = Post.objects.get(id = postID)
        if serializers_comment.is_valid():
 
            serializers_comment.save(author = request.user, post_connected = post)

            return Response(data = serializers_comment.data, status = status.HTTP_201_CREATED)
        return Response(serializers_comment.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes([AuthenticationJWT])
@permission_classes([IsAuthenticated])
def likePost(request, postID):
    if request.method == 'POST':
        user = request.user
        post = Post.objects.get(id = postID)
        serializer = LikePostSerializer(data = request.data)
        if serializer.is_valid():
            if user not in post.liked.all():
               like = serializer.save(user = user, post = post)
               post.save(liked = user)
               return Response(data = serializer.data, status = status.HTTP_201_CREATED)
            else:
                like = serializer.update()
                post.save(liked = like)
                return Response(data = serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['PUT'])
@authentication_classes([AuthenticationJWT])
@permission_classes([IsAuthenticated])
def updateComment(request, id):
    if request.method == 'PUT':
        comment = Comment.objects.get(id = id)
        serializer = CreateComment(instance = comment, data = request.data)       
        if serializer.is_valid():
            serializer.save()

            return Response(data = serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([AuthenticationJWT])
@permission_classes([IsAuthenticated])
def createPostAPI(request):
    if request.method == 'POST':
        serializers = CreatePostSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save(author = request.user)

            return Response(data = serializers.data, status = status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



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

class EditPost(UpdateAPIView):
    authentication_classes = [SessionAuthentication, AuthenticationJWT]
    permission_classes = [IsAuthenticated]
    serializer_class = CreatePostSerializer
    queryset = Post.objects.all()


class DeletePost(DestroyAPIView):
    authentication_classes = [SessionAuthentication, AuthenticationJWT]
    permission_classes = [IsAuthenticated]
    # serializer_class = CreatePostSerializer
    queryset = Post.objects.all()
  
    
@decorators.login_required(login_url='login')
def createComment(request, id):
    print(request.path)
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        form = NewCommentForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post_connected = post
            form.save()
            return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')


def getCommentsByPostID(request, id):
    if request.method == 'GET':
        comments = Comment.objects.filter(post_connected=id)
        return render(request, 'index.html', { 'comment': comments})

# def likePost(request, post)
#######  APIs

class getAllPosts(ListAPIView):
    authentication_classes = [AuthenticationJWT]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    filterset_fields = ['caption']
    serializer_class = GetAllPost
    ordering_fields = ['caption']
    def get_queryset(self):
        queryset = Post.objects.all()
        email = self.request.query_params.get('email', None)
        if email is not None:
            queryset = queryset.filter(author__email=email)
        return queryset
    

    # def get(self, request):
    #     listPosts = Post.objects.all()
    #     serializers_data = GetAllPost(listPosts, many = True)
    #     return Response(data= serializers_data.data, status = status.HTTP_200_OK)

    # def post(self, request):
    #     data = CreatePost(data= request.data)
    #     caption = data.data['caption']
    #     image