from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponseRedirect
from rest_framework import generics, status
from rest_framework import throttling
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PasswordReset, PasswordResetRequestSerializer, UserSerializer, LoginSerializer
from .models import User
from rest_framework.authtoken.models import Token
from .email import Mail
from .tokens import decode_reset_token


class PostAnononymousRateThrottle(throttling.AnonRateThrottle):
    scope = 'post_anon'
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)


class Registration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token', token.key}, status=status.HTTP_201_CREATED)


class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer
    throttle_classes = [PostAnononymousRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, create = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequest(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user_id = User.objects.filter(email=email).first().id
        Mail.send_password_reset_token(email, user_id, request)
        return Response({
            'result': 'see your email'
        })        


class PasswordUpdate(generics.CreateAPIView):
    serializer_class = PasswordReset
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        user_id = decode_reset_token(self.kwargs.get('uidb64'))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(pk=user_id).first()
        password = serializer.validated_data.get('password1')
        user.set_password(password)
        user.save()
        return HttpResponseRedirect(f'{get_current_site}/api/login/')