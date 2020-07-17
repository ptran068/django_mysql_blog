import jwt

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import exceptions, status
# from rest_framework.authentication import TokenAuthentication

from django.http import HttpResponse
from rest_framework.authentication import get_authorization_header, BaseAuthentication

class JSONWebTokenAuthentication(BaseAuthentication):
    # model = User


    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token == "null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
    

    def authenticate_credentials(self, token):
        # white_lists = [
        #     '/api/getPost'
        # ]

        # if self.request.path in self.white_lists:
        #     return True
        try:
            payload = jwt.decode(token, settings.JWT_SECRET)
            user = User.objects.get(email=payload['email'])
        except (jwt.DecodeError, User.DoesNotExist):
            raise exceptions.AuthenticationFailed('Invalid token')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')
        return (user, payload)

    # def authenticate_header(self, request):
    #     return 'Token'