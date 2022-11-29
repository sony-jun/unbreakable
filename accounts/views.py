from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
import requests
import json
from .models import *
from articles.models import *
# Create your views here.

# 임시
def index(request):
    context = {'check':False}
    if request.session.get('access_token'):
        context['check'] = True
    return render(request, 'accounts/index.html', context)

def signup(request):
    # 이미 회원가입한 유저라면 
    # if request.user.is_authenticated:
    #     return redirect("accounts:index")
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect(request.GET.get('next') or 'accounts:index')
    else:
        form = CustomUserCreationForm()
    context = {
        "form":form,
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next") or "accounts:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect("accounts:index")

@login_required
def update(request, user_pk):
    user = get_user_model().objects.get(pk=user_pk)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", user_pk)
    else:
        form = CustomUserChangeForm(instance=user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)

@login_required
def profile(request, user_pk):
    user = get_user_model().objects.get(pk=user_pk)
    articles = user.articles_set.filter(user=user.pk)
    messages = Message.objects.filter(receiver_id=user.pk)
    context = {
        'user':user,
        'articles':articles,
        'messages':messages,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def delete(request, user_pk):
    user = get_user_model().objects.get(pk=user_pk)
    user.delete()
    return redirect("accounts:index")

# 비밀번호 변경
@login_required
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            # 로그인 유지
            update_session_auth_hash(request, request.user.pk)
            return redirect('accounts:profile', request.user.pk)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form,
    }
    return render(request,'accounts/password.html',context)

# 카카오 소셜 로그인
def kakao_request(reqeust):
    kakao_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'
    redirect_uri = "http://localhost:8000/accounts/kakao/login/callback/"
    client_id = 'fdc7989db5f7e970c9ba50edb78ec9a6'
    return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")

def kakao_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": 'fdc7989db5f7e970c9ba50edb78ec9a6',
        "redirect_uri": "http://localhost:8000/accounts/kakao/login/callback/",
        "code": request.GET.get("code"),
    }

    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    access_token = requests.post(kakao_token_api, data=data).json()['access_token']
    
    headers = {"Authorization": f"bearer ${access_token}"}
    kakao_user_api = "https://kapi.kakao.com/v2/user/me"
    kakao_user_information = requests.get(kakao_user_api, headers=headers).json()
    kakao_id = kakao_user_information["id"]
    kakao_nickname = kakao_user_information["properties"]["nickname"]
    kakao_birthday = kakao_user_information["kakao_account"].get("birthday")
    
    # 받아온 kakao 유저정보중 id가 db에 있는지 확인합니다.
    if get_user_model().objects.filter(username=kakao_id).exists():
        kakao_user = get_user_model().objects.get(username=kakao_id)
        # kakao_user.refresh_token = temp["refresh_token"]
        kakao_user.save()
    else:
        kakao_login_user = get_user_model().objects.create(
            username=kakao_id,
            fullname=kakao_nickname,
            birthday=kakao_birthday,
            # refresh_token = temp["refresh_token"],
        )
        kakao_login_user.save()
        kakao_user = get_user_model().objects.get(username=kakao_id)
    auth_login(request, kakao_user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect(request.GET.get("next") or "accounts:index")


def message_create(request, user_pk, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    receiver = User.objects.get(pk=user_pk)
    print(user_pk)
    if request.method == "POST":
        message_form = MessageForm(request.POST)
        if message_form.is_valid:
            message = message_form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.articles = articles
            message.save()
            return redirect('articles:articles_index')
    else:
        message_form = MessageForm()
    context = {
        'receiver':receiver,
        'message_form':message_form,
    }
    return render(request, 'accounts/message_create.html',context)