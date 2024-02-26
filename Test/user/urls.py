from django.contrib import admin
from django.urls import path
from user import views


urlpatterns = [
    path("register/", views.register),
    path("login/", views.user_login),
    path("logout/", views.user_logout),
    path("send_verification/", views.send_email_verification),
    path("check_code/", views.check_code),
    path("password_forget/", views.password_forget),
    path("password_reset/", views.password_reset),
    path("user_set/", views.user_set)
]
