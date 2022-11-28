from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import *
# Create your views here.

# 임시
def index(request):
    return render(request, 'accounts/index.html')

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
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", user_pk)
    else:
        form = CustomUserCreationForm(instance=user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)

@login_required
def profile(request, user_pk):
    user = get_user_model().objects.get(pk=user_pk)
    context = {
        'user':user,
    }
    return render(request, 'accounts/profile.html', context)