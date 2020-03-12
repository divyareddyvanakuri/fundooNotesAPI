from rest_framework import serializers
from .models import Person,Note
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

class DisplayNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model =Note
        fields = "__all__"
        read_only_fields = ["user"]
        

class CreateNoteSerializer(serializers.ModelSerializer):
     class Meta:
        model =Note
        fields = ['title','text','archive','pinnote']

class RestoreNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model =Note
        fields = ['trash']
