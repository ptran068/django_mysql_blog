from django.urls import path
from .views import (createUser, login, logout)

urlpatterns = [
    path('register', createUser, name = 'register'),
    path('login', login, name = 'login'),
    path('logout',logout, name='logout'),

]
