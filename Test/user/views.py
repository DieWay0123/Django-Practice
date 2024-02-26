import string
from django.shortcuts import render
from .models import UserProfile, UserSet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from Test.settings import EMAIL_HOST_USER
from datetime import timedelta
from random import randint, choice
import uuid
import json


def index(request):
    return render(request, "user/index.html")


@csrf_exempt
def register(request):
    if request.method == "POST":
        data = request.POST
        try:
            uid = uuid.uuid1()
            user = UserProfile.objects.create_user(uid=uid, username=data["account"], phone=data["phone"],
                                                   email=data["email"], is_active=False)
            user.database = UserSet.objects.create(uid=uid, name=data["account"],
                                                   phone=data["phone"], email=data["email"])
            user.set_password(data["password"])
            user.save()
            message = {"status": "0"}
        except Exception as e:
            print(e)
            message = {"status": "1"}
        return JsonResponse(message)


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        data = request.POST
        auth_user = authenticate(username=data["account"], password=data["password"])
        if auth_user:  # is_active
            request.session.create()
            request.session["uid"] = auth_user.uid
            login(request, auth_user)
            message = {"status": "0", "session_id": request.session.session_key}
        else:
            message = {"status": "1", "content": "fail to login"}

        return JsonResponse(message)


@csrf_exempt
def user_logout(request):
    try:
        logout(request)
        message = {"status": "0"}
    except Exception as e:
        print(e)
        message = {"status": "1"}
    return JsonResponse(message)


@csrf_exempt
def send_email_verification(request):
    if request.method == "POST":
        data = request.POST
        user = UserProfile.objects.get(email=data["email"])
        if request.user.is_authenticated or user.is_active:
            message = {"status": "1", "content": "the email has been verification."}
        else:
            try:
                code = randint(100000, 999999)
                request.session["verification_code"] = code
                request.session.set_expiry(timedelta(minutes=5))
                # print(request.session.get_expiry_age())
                send_mail("帳號驗證信", "Your verification code is " + str(code), EMAIL_HOST_USER, [data["email"]])
                message = {"status": "0", "verification code": code}
            except Exception as e:
                print(e)
                message = {"status": "1", "content": "fail to send mail"}
        return JsonResponse(message)


@csrf_exempt
def check_code(request):
    if request.method == "POST":
        data = request.POST
        if str(request.session["verification_code"]) == data["answer"]:
            try:
                user = UserProfile.objects.get(email=data["email"])
                user.is_active = True
                user.save()
                message = {"status": "0", "username": user.username}
            except Exception as e:
                print(e)
                message = {"status": "1"}
        else:
            message = {"status": "1", "content": "wrong verification code"}
        return JsonResponse(message)


@csrf_exempt
def password_forget(request):
    if request.method == "POST":
        data = request.POST
        try:
            user = UserProfile.objects.get(email=data["email"])
            code_list = string.ascii_letters + string.digits
            code = [choice(code_list) for i in range(10)]
            user.set_password("".join(code))
            user.save()
            send_mail("密碼重設通知", "你的帳號已被修改為" + "".join(code), EMAIL_HOST_USER, [data["email"]])
            message = {"status": "0", "password": "".join(code)}
        except Exception as e:
            print(e)
            message = {"status": "1"}
        return JsonResponse(message)


@csrf_exempt
def password_reset(request):  # 改session或許好點
    if request.method == "POST":
        data = request.POST
        if request.user.is_authenticated:
            try:
                user = UserProfile.objects.get(uid=data["token"])
                user.set_password(data["password"])
                user.save()
                message = {"status": "0", "new Password": data["password"]}
            except Exception as e:
                print(e)
                message = {"status": "1", "content": "fail to reset password"}
        else:
            message = {"status": "1", "content": "please log in"}
        return JsonResponse(message)


@csrf_exempt
def user_set(request):
    if request.method == "PATCH":
        data = request.body
        data = json.loads(data)
        try:
            user = UserSet.objects.get(uid=request.session["uid"])

            user.name = data.get("name", user.name)
            user.birthday = data.get("birthday", user.birthday)
            user.height = data.get("height", user.height)
            user.gender = data.get("gender", user.gender)
            user.fcm_id = data.get("fcm_id", user.fcm_id)
            user.address = data.get("address", user.address)
            user.weight = data.get("weight", user.weight)
            user.phone = data.get("phone", user.phone)
            user.email = data.get("email", user.email)
            user.save()

            message = {"status": "0"}
        except Exception as e:
            print(e)
            message = {"status": "1"}
        return JsonResponse(message)
