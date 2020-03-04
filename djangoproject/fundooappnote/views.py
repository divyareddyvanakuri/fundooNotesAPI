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
from .serializers import RegisterSerializer, LoginSerializer, SetPasswordSerializer, UserSerializer,ForgotPasswordSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth
from .token_activation import tokenActivation,passwordActivation
from django.views.decorators.csrf import csrf_exempt
import jwt

# Create your views here.
class CreateUser(GenericAPIView):
    serializer_class = RegisterSerializer
    @ csrf_exempt
    def post(self, request):
        #print(request.data)
        username=request.data['username']
        email = request.data['email']
        password = request.data['password']
        confirmpassword = request.data['confirmpassword']
        if password == confirmpassword:
            if User.objects.filter(email=email).count() == 0:
                user=User.objects.create_user(username=username, email=email, password=password)
                user.save()
                token = tokenActivation(username,password)
                print(token)
                current_site = get_current_site(request)
                domain_name = current_site.domain
                # print(jwt.decode(token,'SECRET_KEY')) 
                url = str(token)
                # print("url:",url)
                surl = get_surl(url)
                # print("surl:",surl)
                z=surl.split("/")
                # print(z[2])
                mail_subject = "Activate your account"
                msg = render_to_string('email_validation.html', {
               'username': username,
               'domain': domain_name,
               'surl': z[2]
                })
                print("msg",msg)
                send_mail(mail_subject,msg,EMAIL_HOST_USER,[email],fail_silently=False,) 
                return Response('successfully registered,please activate your accout')
            return HttpResponse('user is already existed')
        return HttpResponse("password mismatch")

def activate(request, surl):   
    print("surl :", surl)
    return redirect('/login/')

class LoginUser(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        #print(request.data)
        username=request.data['username']
        #print(username)
        password=request.data['password']
        #print(password)
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return Response("successfully logged in")
        return HttpResponse("Invalide login user details")

class ForgotPassword(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        email = request.data['email']
        if User.objects.filter(email=email).count() == 0:
            return HttpResponse("invalide user")
    
        user = User.objects.get(email=email)
        username = user.username
        print(username)
        token = passwordActivation(username)
        print(token)
        current_site = get_current_site(request)
        domain_name = current_site.domain
        print(jwt.decode(token,'SECRET_KEY')) 
        url = str(token)
        print("url:",url)
        surl = get_surl(url)
        print("surl:",surl)
        z=surl.split("/")
        print(z[2])
        mail_subject = "Activate your account"
        msg1 = render_to_string('passwordactivation.html', {
        'username': username,
        'domain': domain_name,
        'surl': z[2]
        })
        print("msg",msg1)
        send_mail(mail_subject,msg1,EMAIL_HOST_USER,[email],fail_silently=False,) 
        return HttpResponse('successfully reseted the password')