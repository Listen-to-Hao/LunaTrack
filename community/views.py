from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from users.models import UserProfile

def post_list(request):
    """返回帖子列表，支持分页"""
    page = request.GET.get("page", 1)
    search_query = request.GET.get("q", "").strip()

    posts = Post.objects.all().order_by("-created_at")
    if search_query:
        posts = posts.filter(content__icontains=search_query)

    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(page)

    post_data = [{
        "id": post.id,
        "author": post.author.nickname or post.author.username,
        "author_avatar": post.author.avatar.url if post.author.avatar else "/static/images/default_avatar.jpg",
        "content": post.content,
        "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
        "likes_count": post.likes.count(),
        "comments_count": post.comments.count(),
        "collections_count": post.collections.count(),
        "image_url": post.images.url if post.images else None
    } for post in page_obj]

    return JsonResponse({
        "success": True,
        "posts": post_data,
        "has_next": page_obj.has_next()
    })

@login_required
def create_post(request):
    """创建新帖子"""
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        image = request.FILES.get("images")

        if not content:
            return JsonResponse({"success": False, "message": "Content cannot be empty!"}, status=400)

        post = Post.objects.create(author=request.user, content=content, images=image)

        return JsonResponse({
            "success": True,
            "message": "Post created successfully!",
            "post": {
                "id": post.id,
                "author": post.author.nickname or post.author.username,
                "author_avatar": post.author.avatar.url if post.author.avatar else "/static/images/default_avatar.jpg",
                "content": post.content,
                "created_at": post.created_at.strftime("%Y-%m-%d %H:%M"),
                "likes_count": 0,
                "comments_count": 0,
                "collections_count": 0,
                "image_url": post.images.url if post.images else None
            }
        })

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

def discover_view(request):
    """社区发现页面"""
    return render(request, 'community/discover.html')


@login_required
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)  # 取消点赞
        liked = False
    else:
        post.likes.add(request.user)  # 添加点赞
        liked = True

    return JsonResponse({"success": True, "liked": liked, "likes_count": post.likes.count()})

@login_required
def collect_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.collections.filter(id=request.user.id).exists():
        post.collections.remove(request.user)  # 取消收藏
        collected = False
    else:
        post.collections.add(request.user)  # 添加收藏
        collected = True

    return JsonResponse({"success": True, "collected": collected, "collections_count": post.collections.count()})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if not content:
            return JsonResponse({"success": False, "message": "❌ Comment cannot be empty!"}, status=400)

        comment = Comment.objects.create(post=post, author=request.user, content=content)
        return JsonResponse({
            "success": True,
            "comment": {
                "author": request.user.username,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M")
            }
        })

    elif request.method == "GET":
        comments = post.comments.all().order_by("-created_at")
        comment_data = [
            {"author": c.author.username, "content": c.content, "created_at": c.created_at.strftime("%Y-%m-%d %H:%M")}
            for c in comments
        ]

        return JsonResponse({"success": True, "comments": comment_data})
