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
from rest_framework import permissions
from .utils import UserPermissions, PostAnononymousRateThrottle


class Registration(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token', token.key}, status=status.HTTP_201_CREATED)


class Login(generics.CreateAPIView):
    serializer_class = LoginSerializer
    throttle_classes = [PostAnononymousRateThrottle]
    permission_classes = [UserPermissions]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, create = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequest(generics.CreateAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [UserPermissions]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user_id = User.objects.filter(email=email).first().id
        Mail.send_password_reset_token(email, user_id, request)
        return Response({
            'result': 'see your email'
        })        


class PasswordUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = PasswordReset
    permission_classes = [UserPermissions]

    def get(self, request, *args, **kwargs):
        user_id = decode_reset_token(self.kwargs.get('uidb64'))
        currect_site = get_current_site(request)
        if not User.objects.filter(pk=user_id).exists():
            return HttpResponseRedirect(f'http://{currect_site}/api/login/')
        else:
            return Response({'result': 'update your password'}, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        user_id = decode_reset_token(self.kwargs.get('uidb64'))
        current_site = get_current_site(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(pk=user_id).first()
        password = serializer.validated_data.get('password1')
        try:
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(f'http://{current_site}/api/login/')
        except:
            return Response({'result': 'პაროლის განსაახლებელ ტოკენს დრო გაუვიდა სცადეთ თავიდან'})

class DeleteAccount(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


    def delete(self, request, *args, **kwargs):
        user=self.request.user
        user.delete()

        return Response({"result":"მომხარებელი წაიშალა"})