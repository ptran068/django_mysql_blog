from django.urls import path
from .views import  logout, HandleLogin

urlpatterns = [
    path('login', HandleLogin.as_view(), name = 'login'),
    path('logout',logout, name='logout'),

]
