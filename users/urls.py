from django.urls import path
from .views import (createUser, login)

urlpatterns = [
    path('create/', createUser),
    path('login/', login),
]
