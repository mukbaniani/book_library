from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(style={'input_type': 'password'},
    write_only=True, 
    label='პაროლი')
    password2 = serializers.CharField(style={'input_type': 'password'}, 
    write_only=True,
    label='გაიმეორეთ პაროლი')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'passport_id', 'password1', 'password2']

    def validate(self, attrs):
        if attrs.get('password1') != attrs.get('password2'):
            raise serializers.ValidationError('პაროლი ერთნამენთს არ ემთხვევა')
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