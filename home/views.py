from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(req):
    return render(req, 'pages/home.html')

def contact(req):
   return render(req, 'pages/contact.html')