from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from djangoproject.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer,SetPasswordSerializer,UserSerializer,ForgotPasswordSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
from .token_activation import tokenActivation, passwordActivation
from django.views.decorators.csrf import csrf_exempt
import jwt


# Create your views here.
class CreateUser(GenericAPIView):
    serializer_class = RegisterSerializer
    @ csrf_exempt
    def post(self, request):
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        confirmpassword = request.data['confirmpassword']
        if password == confirmpassword:
            if User.objects.filter(email=email).count() == 0:
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                token = tokenActivation(username, password)
                print(token)
                current_site = get_current_site(request)
                domain_name = current_site.domain
                # print(jwt.decode(token,'SECRET_KEY'))
                url = str(token)
                surl = get_surl(url)
                z = surl.split("/")
                mail_subject = "Activate your account"
                msg = render_to_string('email_validation.html', {'username': username,'domain': domain_name,'surl': z[2]})
                print("msg", msg)
                send_mail(mail_subject, msg, EMAIL_HOST_USER,
                          [email], fail_silently=False,)
                return Response('successfully registered,please activate your accout')
            return HttpResponse('user is already existed')
        return HttpResponse("password mismatch")


def activate(request, surl):
    print("surl :", surl)
    return redirect('/login/')


class LoginUser(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return Response("successfully logged in")
        return Response("Invalide user")


class ForgotPassword(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        email = request.data['email']
        if User.objects.filter(email=email).count() == 0:
            return Response("invalide user")

        user = User.objects.get(email=email)
        username = user.username
        print(username)
        token = passwordActivation(username)
        current_site = get_current_site(request)
        domain_name = current_site.domain
        print(jwt.decode(token, 'SECRET_KEY'))
        url = str(token)
        surl = get_surl(url)
        z = surl.split("/")
        mail_subject = "Activate your account"
        msg1 = render_to_string('password_activation.html', {'username': username,'domain': domain_name,'surl': z[2]})
        print("msg", msg1)
        send_mail(mail_subject, msg1, EMAIL_HOST_USER,
                  [email], fail_silently=False,)
        return Response(msg1)


class ResetPassword(GenericAPIView):
    serializer_class = SetPasswordSerializer

    def post(self, request):
        username = self.request.user.username
        newpassword = request.data['password']
        confirmpassword = request.data['confirmpassword']
        user_count = User.objects.filter(username=username).count()
        if newpassword == confirmpassword and user_count == 1:
            user = User.objects.get(username=username)
            user.set_password(newpassword)
            user.save()
            return Response("you are succesfully reseted the account password")
        return Response("please login ,before reset your password")


def passwordactivation(request, surl):
    print("surl :", surl)
    url = ShortURL.objects.get(surl=surl)
    token = url.lurl
    username = jwt.decode(token, 'SECRET_KEY')
    print(username)
    return redirect('/reset/')

def logout(request):
    auth.logout(request)
    return HttpResponse('you are successfully logged out from your account')