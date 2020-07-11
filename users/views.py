from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User, auth
from django.views import View
# Create your views here.
        
def logout(request):
    auth.logout(request)
    return redirect('/')

class HandleLogin(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email=request.POST['email']
        password=request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, "invalild username or password")
            return redirect('login')