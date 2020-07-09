from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('profile_posts', views.profile_posts, name='profile_posts'),
    
    # path('create', createPostView.as_view())
]
