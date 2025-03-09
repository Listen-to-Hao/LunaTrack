from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserProfile
from .forms import RegisterForm, UserProfileForm, EditProfileForm
from community.models import Post

def register(request):
    """ 用户注册视图 """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

def user_login(request):
    """ 用户登录视图 """
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

def user_logout(request):
    """ 用户登出视图 """
    logout(request)
    return redirect("home")

@login_required
def me_view(request):
    """ 个人主页视图（仅展示，不处理修改） """
    user = request.user

    context = {
        "user": user,
        "avatar_url": user.avatar.url if user.avatar else "/media/avatars/default.jpg",  # ✅ 使用默认头像
    }
    return render(request, "users/me.html", context)

@login_required
def edit_profile(request):
    """ 编辑个人信息（异步更新） """
    if request.method == "POST":
        user = request.user
        form = EditProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Profile updated successfully!"})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)
