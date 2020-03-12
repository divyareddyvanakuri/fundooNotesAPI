from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django_short_url.views import get_surl
from django_short_url.models import ShortURL
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from djangoproject.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, SetPasswordSerializer, UserSerializer, ForgotPasswordSerializer, CreateNoteSerializer, DisplayNoteSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, auth, UserManager
from .models import Note
from .token_activation import tokenActivation, passwordActivation
from django.views.decorators.csrf import csrf_exempt
import jwt
from rest_framework import status
from django.utils.datastructures import MultiValueDictKeyError
# objects = UserManager()
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
                current_site = get_current_site(request)
                domain_name = current_site.domain
                surl = get_surl(str(token))
                z = surl.split("/")
                mail_subject = "Activate your account"
                msg = render_to_string('email_validation.html', {
                    'username': username, 'domain': domain_name, 'surl': z[2]})
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
                return Response("logged in successfully")
        return Response("Invalide user")


class ForgotPassword(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        email = request.data['email']
        if User.objects.filter(email=email).count() == 0:
            return Response("invalide user")
        user = User.objects.get(email=email)
        username = user.username
        token = passwordActivation(username)
        current_site = get_current_site(request)
        domain_name = current_site.domain
        surl = get_surl(str(token))
        z = surl.split("/")
        mail_subject = "Activate your account"
        msg1 = render_to_string('password_activation.html', {
            'username': username, 'domain': domain_name, 'surl': z[2]})
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
            return Response("you are successfully reseted the account password")
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


class CreateNote(GenericAPIView):

    serializer_class = CreateNoteSerializer

    def post(self, request):
        try:
            user = User.objects.get(username=self.request.user.username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        pk = user.id
        title = request.data['title']
        text = request.data['text']
        if 'archive' in request.POST:
            archive = request.POST['archive']
            if archive == 'true':
                archive = True
        else:
            archive = False
        print(archive)
        if 'pinnote' in request.POST :
            pinnote = request.POST['pinnote']
            if pinnote == 'true':
                pinnote = True
        else:
            pinnote = False
        print(pinnote)
        if 'trash' in request.POST :
            trash = request.POST['trash']
            if trash == 'true':
                trash = True
        else:
            trash = False
        print(trash)
        note = Note(user=user, title=title, text=text,
                    archive=archive, pinnote=pinnote,trash=trash)
        note.save()
        return Response("Added note successfully fo fundooapp ")


class DisplayNote(GenericAPIView):

    def get(self, requset):
        try:
            user = User.objects.get(username=self.request.user.username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        note = Note.objects.filter(user_id=user.id)
        serializer = DisplayNoteSerializer(note, many=True)
        return Response(serializer.data)


class UpdateNote(GenericAPIView):

    serializer_class = DisplayNoteSerializer

    def get(self, request, pk):
        try:
            user = User.objects.get(username=request.user.username)
            note = Note.objects.get(pk=pk, user_id=user.id)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = DisplayNoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            user = User.objects.get(username=request.user.username)
            note = Note.objects.get(pk=pk, user_id=user.id)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            title = request.data['title']
            text = request.data['text']
        except MultiValueDictKeyError:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if 'archive' in request.POST:
            archive = request.POST['archive']
            if archive == 'true':
                archive = True
        else:
            archive = False
        print(archive)
        if 'pinnote' in request.POST :
            pinnote = request.POST['pinnote']
            if pinnote == 'true':
                pinnote = True
        else:
            pinnote = False
        print(pinnote)
        if 'trash' in request.POST :
            trash = request.POST['trash']
            if trash == 'true':
                trash = True
        else:
            trash = False
        print(trash)
        try:
            Note.objects.filter(pk=pk, user_id=user.id).update(
                title=title, text=text, archive=archive, pinnote=pinnote,trash=trash)

            return Response("updated")
        except Exception:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class DeleteNote(GenericAPIView):

    def delete(self, request, pk):
        try:
            user = User.objects.get(username=request.user.username)
            note = Note.objects.get(pk=pk, user_id=user.id)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def archive_detail(request):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    note = Note.objects.filter(user_id=user.id, archive=True)
    serializer = DisplayNoteSerializer(note, many=True)
    return Response(serializer.data)
