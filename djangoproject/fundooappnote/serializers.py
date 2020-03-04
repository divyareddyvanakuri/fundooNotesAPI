from rest_framework import serializers
from .models import Person
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['username', 'password']


class SetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['password', 'confirmpassword']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['username']


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['email']
