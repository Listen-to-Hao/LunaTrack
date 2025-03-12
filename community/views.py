from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Comment
from users.models import UserProfile

def post_list(request):
    try:
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
            "likes_count": post.liked_by.count(),
            "comments_count": post.comments.count(),
            "collections_count": post.collected_by.count(),
            "image_url": post.image.url if post.image else None
        } for post in page_obj]

        return JsonResponse({
            "success": True,
            "posts": post_data,
            "has_next": page_obj.has_next()
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)

@login_required
def create_post(request):
    try:
        if request.method == "POST":
            content = request.POST.get("content", "").strip()
            image = request.FILES.get("image")

            if not content:
                return JsonResponse({
                    "success": False,
                    "message": "Content cannot be empty!"
                }, status=400)

            post = Post.objects.create(author=request.user, content=content, image=image)

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
                    "image_url": post.image.url if post.image else None
                }
            })

        return JsonResponse({
            "success": False,
            "message": "Invalid request method."
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)

def discover_view(request):
    """社区发现页面"""
    return render(request, 'community/discover.html')

@login_required
def like_post(request, post_id):
    try:
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
            "likes_count": post.liked_by.count()
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)

@login_required
def collect_post(request, post_id):
    try:
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
            "collections_count": post.collected_by.count()
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)

@csrf_exempt
def post_comment(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)

        if request.method == "GET":
            # 获取评论
            comments = post.comments.all().order_by("-created_at")
            comment_data = [{
                "id": comment.id,
                "author": comment.author.nickname or comment.author.username,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M")
            } for comment in comments]

            return JsonResponse({
                "success": True,
                "comments": comment_data
            })

        elif request.method == "POST":
            # 提交评论
            if not request.user.is_authenticated:
                return JsonResponse({
                    "success": False,
                    "message": "You must be logged in to comment."
                }, status=403)

            content = request.POST.get("content", "").strip()
            if not content:
                return JsonResponse({
                    "success": False,
                    "message": "Comment cannot be empty."
                }, status=400)

            comment = Comment.objects.create(post=post, author=request.user, content=content)

            return JsonResponse({
                "success": True,
                "comment": {
                    "id": comment.id,
                    "author": comment.author.nickname or comment.author.username,
                    "content": comment.content,
                    "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M")
                },
                "comments_count": post.comments.count()
            })

        return JsonResponse({
            "success": False,
            "message": "Invalid request method."
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)