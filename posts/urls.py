from django.urls import path
from . import views
from .views import CreatePost, PostDetail, getAllPosts, CustomAuthToken, EditPost, DeletePost

urlpatterns = [
    path('',views.base, name = 'base'),
    path('register', views.createUser, name = 'register'),

    path('index', views.index, name= 'index'),
    path('post/<int:pk>/',PostDetail.as_view(), name = 'post_details' ),

    path('post/create', CreatePost.as_view(), name = 'create-post'),
    path('comment/<int:id>', views.createComment, name = 'comment'),
    path('get-comment/<int:id>', views.createComment, name = 'get-comment'),
    path('api/posts', getAllPosts.as_view()),
    path('api/posts/<int:pk>', EditPost.as_view()),
    path('api/posts/delete/<int:pk>', DeletePost.as_view()),

    path('api-token-auth', CustomAuthToken.as_view()),
    path('api/comment/<int:postID>', views.createCommentByApis),
    path('api/post', views.createPostAPI),

]
