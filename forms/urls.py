"""forms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('forms/', views.forms),
    path('set/session/', views.set_cookie),
    path('login/', views.login),
    path('home/', views.home),
    path('index/', views.index),
    path('logout/', views.logout),
    path('login/superuser', views.login_superuser),
    path('test/', views.test),
    path('register/', views.register),
    path('set_password/', views.set_password),
    path('logout/', views.out_log),
]
