from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User, auth
# Create your views here.

@require_http_methods(['POST', 'GET'])
def createUser(request):
    if request.method == 'GET':
        return render(request, 'pages/createUser.html')
    elif request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username taken")
                return redirect ('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email taken")
                return redirect('register')
            else:    
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save();
                return redirect('index')

                    
        else:
            messages.info(request, "password not matching")
            return redirect('register')

    else:
        return render(request, 'pages/createUser.html')

    
################################################
@require_http_methods(['POST', 'GET'])
def login(request):
    if request.method == 'GET':
        return render(request, 'pages/login.html')
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, "invalild username or password")
            return redirect('login')
    else:
        return render(request, 'base.html')

##############################################
        
def logout(request):
    auth.logout(request)
    return redirect('/')