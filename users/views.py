from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .forms import (CreateUser)
from .models import User
# Create your views here.

# @require_http_methods(["GET"])
# def getPageRegister(req):
#     return render(req, 'pages/createUser.html')

@require_http_methods(["GET"])
def login(req):
    return render(req, 'pages/login.html')

@require_http_methods(['POST', 'GET'])
def createUser(req):
    if req.method == 'POST':
        form = CreateUser(req.POST)
        if form.is_valid():
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            form.save()
            return render(req, 'pages/createUser.html')
    else:
        return render(req, 'pages/createUser.html')

    
#raise same same with throw error
#raise TypeError("Only integers are allowed")