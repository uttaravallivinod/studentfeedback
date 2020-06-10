"""fback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from feedback import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('login',views.login),
    path('register',views.register),
    path('extra',views.extra),
    path('profile',views.profile),
    path('accounts/',include('django.contrib.auth.urls')),
    path('addcourse',views.addcourse),
    path('student',views.student),
    path('upload',views.upload),
    path('faculty',views.faculty),
    path('uploadfaculty',views.uploadfaculty),
    path('teach',views.teach),
    path('link',views.link),
    path('sauth',views.sauth),
    path('feed/<slug:stslug>/<slug:clslug>',views.feed),
    path('otpvalid',views.otpvalid),
    path('uploadcourse',views.uploadcourse),
    path('cdelete/<slug:slugg>/',views.cdelete),
    path('fdelete/<slug:slugg>/',views.fdelete),
    path('updateteach/',views.updateteach),
    path('cupdate/<slug:slugg>/',views.cupdate),
    path('fupdate/<slug:slugg>',views.fupdate),
    path('dashboard',views.anal),
    path('fdashboard/<slug:slugg>',views.fanal),
    path('pp',views.pp),
    path('alert',views.alert),
    path('sms',views.sms)

]
