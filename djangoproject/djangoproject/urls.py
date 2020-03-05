"""djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fundooappnote import views
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='fundooNotes API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.CreateUser.as_view()),
    path('activate/<slug:surl>/', views.activate, name='activate'),
    path('login/', views.LoginUser.as_view()),
    path('forgot/', views.ForgotPassword.as_view()),
    path('passwordactivation/<slug:surl>/',
         views.passwordactivation, name='passwordactivation'),
    path('reset/',views.ResetPassword.as_view()),
    path('logout/',views.logout),
    url(r'^$', schema_view),
]
