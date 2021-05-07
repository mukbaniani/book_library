from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(style={'input_type': 'password'},
    write_only=True, 
    label=_('პაროლი'))
    password2 = serializers.CharField(style={'input_type': 'password'}, 
    write_only=True,
    label=_('გაიმეორეთ პაროლი'))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'passport_id', 'password1', 'password2']

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 == password2:
            if len(password1) < 8:
                error_message = 'მინიმალური ასეობის რაოდენობა 8'
                raise serializers.ValidationError(error_message)
        if password1 != password2:
            error_message = 'პაროლი ერთნამენთს არ ემთხვევა'
            raise serializers.ValidationError(error_message)
        return attrs

    def create(self, validated_data):
        user = User(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            phone = validated_data['phone'],
            passport_id = validated_data['passport_id'],
            address = validated_data['address']
        )
        password1 = self.validated_data.get('password1')
        user.set_password(password1)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_('მეილი'),
        write_only=True
    )
    password = serializers.CharField(
        label=_('პაროლი'),
        write_only=True,
        style={'input_type':'password'}
    )
    token = serializers.CharField(
        label=_('token'),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), 
                                email=email, password=password)
            if not user:
                error_message = 'მსგავსი მომხმარებელი არ მოიძებნა'
                raise serializers.ValidationError(error_message)
        else:
            error_message = 'მეილის და პაროლის შევსება აუცილებელია'
            raise serializers.ValidationError(error_message)

        attrs['user'] = user
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label = _('პაროლის აღსადგენად შეიყვანეთ მეილი'),
        write_only=True
    )
    

    def validate(self, attrs):
        email = attrs.get('email')

        if email:
            user = User.objects.filter(email=email).first()
            if not user:
                error_message = 'მეილი ვერ მოიძებნა'
                raise serializers.ValidationError(error_message)
        else:
            error_message = 'პაროლის განსაახლებლად მეილის შეყვანა აუცილებელია'
            raise serializers.ValidationError(error_message)

        attrs['user'] = user
        return attrs


class PasswordReset(serializers.Serializer):
    password1 = serializers.CharField(
        label=_('შეიყვანეთ ახალი პაროლი'),
        write_only = True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        label=_('გაიმეორეთ პაროლი'),
        write_only = True,
        style = {'input_type': 'password'}
    )

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if password2 == password1:
            if len(password1) < 8:
                error_message = 'პაროლი მინიმუმ 8 სიმბოლოს უნდა შეიცავდეს'
                raise serializers.ValidationError(error_message)

        if password1 and password2:
            if password1 != password2:
                error_message = 'პაროლი არ ემთხვევა'
                raise serializers.ValidationError(error_message)
        else:
            error_message = 'პაროლის ველის შევსება აუცილებელია'
            raise serializers.ValidationError(error_message)
        return attrs