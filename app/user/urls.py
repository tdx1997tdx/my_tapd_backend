"""my_tapd_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from .views import *

urlpatterns = [
    path('login', Login.as_view()),
    path('regist', Regist.as_view()),
    path('report', Report.as_view()),
    path('getUserByUsername', GetUserByUsername.as_view()),
    path('getUser', GetUser.as_view()),
    path('updateUserByUsername', UpdateUserByUsername.as_view()),
    path('getImage/<str:uri>', GetImage.as_view()),
    path('uploadImage', UploadImage.as_view()),
]
