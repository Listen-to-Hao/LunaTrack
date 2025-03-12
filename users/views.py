from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserProfile
from .forms import RegisterForm, UserProfileForm, EditProfileForm
from community.models import Post, Comment

# 🌸 获取帖子数据
@login_required
def get_posts(request):
    post_type = request.GET.get("type", "created")
    user = request.user

    if post_type == "created":
        posts = Post.objects.filter(author=user)
    elif post_type == "liked":
        posts = Post.objects.filter(liked_by=user)
    elif post_type == "commented":
        posts = Post.objects.filter(comments__author=user).distinct()
    elif post_type == "collected":
        posts = Post.objects.filter(collected_by=user)
    else:
        return JsonResponse({"error": "Invalid post type"}, status=400)

    posts_data = [
        {
            "id": post.id,
            "author": post.author.nickname or post.author.username,
            "author_avatar": post.author.avatar.url if post.author.avatar else "/static/images/default_avatar.png",
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M") if post.created_at else "Unknown Time",
            "content": post.content,
            "image": post.image.url if post.image else None,
            "likes": post.likes_count,
            "collections": post.collections_count,
            "comments_count": post.comments.count(),
            "comments": [
                {
                    "id": c.id,
                    "user": c.author.nickname or c.author.username,
                    "text": c.content,
                    "avatar": c.author.avatar.url if c.author.avatar else "/static/images/default_avatar.png",
                    "is_author": c.author == user,
                }
                for c in post.comments.all()
            ],
            "is_author": post.author == user,
        }
        for post in posts
    ]

    return JsonResponse({"posts": posts_data})


# 🌸 点赞帖子
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
        liked = False
    else:
        post.liked_by.add(request.user)
        liked = True

    return JsonResponse({
        "success": True,
        "liked": liked,
        "likes": post.likes_count
    })

# 🌸 收藏帖子
@login_required
def collect_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.collected_by.filter(id=request.user.id).exists():
        post.collected_by.remove(request.user)
        collected = False
    else:
        post.collected_by.add(request.user)
        collected = True

    return JsonResponse({
        "success": True,
        "collected": collected,
        "collections": post.collections_count
    })

# 🌸 发布评论
@login_required
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if not content:
            return JsonResponse({"success": False, "message": "Comment cannot be empty."}, status=400)

        comment = Comment.objects.create(post=post, author=request.user, content=content)

        return JsonResponse({
            "success": True,
            "comment": {
                "id": comment.id,
                "user": comment.author.nickname or comment.author.username,
                "text": comment.content,
                "is_author": True
            },
            "comments_count": post.comments.count()
        })

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

# 🌸 删除帖子
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return JsonResponse({"success": True, "message": "Post deleted successfully!"})

# 🌸 删除评论
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    comment.delete()
    return JsonResponse({"success": True, "message": "Comment deleted successfully!"})

# 🌸 用户注册
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    
    # 将表单和错误信息传递给模板
    return render(request, "users/register.html", {"form": form})

# 🌸 用户登录
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

# 🌸 用户登出
def user_logout(request):
    logout(request)
    return redirect("home")

# 🌸 个人主页
@login_required
def me_view(request):
    user = request.user

    context = {
        "user": user,
    }
    return render(request, "users/me.html", context)

# 🌸 编辑个人信息
@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        form = EditProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Profile updated successfully!"})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)
