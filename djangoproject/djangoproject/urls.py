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
    path('register/', views.CreateUser.as_view(),name='register'),
    path('activate/<slug:surl>/', views.activate, name='activate'),
    path('login/', views.LoginUser.as_view(),name='login'),
    path('forgotpassword/', views.ForgotPassword.as_view(),name='forgotpassword'),
    path('passwordactivation/<slug:surl>/',
         views.passwordactivation, name='passwordactivation'),
    path('resetpassword/',views.ResetPassword.as_view(),name='resetpassword'),
    path('logout/',views.logout,name='logout'),
    path('createnote/',views.CreateNote.as_view(),name='createnote'),
    path('editnote/<int:pk>', views.UpdateNote.as_view(),name='editnote'),
    path('deletenote/<int:pk>', views.DeleteNote.as_view(),name='deletenote'),
    path('archive/', views.archive_detail,name='archive'),
    path('displaynote/', views.DisplayNote.as_view(),name='displaynote'),
    path('trash/',views.trash_detail,name='trash'),
    path('pinnote/',views.pinnote_detail,name='pinnote'),
    path('restore/<int:pk>',views.RestoreNote.as_view(),name='restore'),
    url(r'^$', schema_view),
]