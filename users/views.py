from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views import View
from django.conf import settings
from rest_framework import parsers, renderers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AuthCustomTokenSerializer
import datetime
import jwt

from rest_framework.authtoken.views import ObtainAuthToken

class JSONWebTokenAuth(ObtainAuthToken):
    # throttle_classes = ()
    # permission_classes = ()
    # parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    # renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthCustomTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            payload = {
                'email': user.email,
                'iat': datetime.datetime.utcnow(),
                # 'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
            }
            token = jwt.encode(payload, settings.SECRET_KEY)

            payloadRefreshToken = {
                'email': user.email,
                'iat': datetime.datetime.utcnow(),
                # 'nbf': datetime.datetime.utcnow() + datetime.timedelta(minutes=-5),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
            }
            refreshToken = jwt.encode(payloadRefreshToken, settings.REFRESH_JWT_SECRET)

            return Response({
                'token': token,
                'refreshToken': refreshToken
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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