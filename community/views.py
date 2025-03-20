from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Comment
from users.models import UserProfile

def post_list(request):
    try:
        # Get page number and search query from GET request parameters
        page = request.GET.get("page", 1)
        search_query = request.GET.get("q", "").strip()

        # Fetch all posts ordered by creation date
        posts = Post.objects.all().order_by("-created_at")
        if search_query:
            # Filter posts based on search query
            posts = posts.filter(content__icontains=search_query)

        # Paginate the posts, displaying 5 posts per page
        paginator = Paginator(posts, 5)
        page_obj = paginator.get_page(page)

        # Prepare post data for JSON response
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

        # Return paginated posts in JSON format
        return JsonResponse({
            "success": True,
            "posts": post_data,
            "has_next": page_obj.has_next()
        })
    except Exception as e:
        # Return error message if an exception occurs
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)

@login_required
def create_post(request):
    try:
        # Handle POST request for creating a new post
        if request.method == "POST":
            content = request.POST.get("content", "").strip()
            image = request.FILES.get("image")

            # Check if content is empty
            if not content:
                return JsonResponse({
                    "success": False,
                    "message": "Content cannot be empty!"
                }, status=400)

            # Create a new post and return its details in the response
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

        # Return error if request method is not POST
        return JsonResponse({
            "success": False,
            "message": "Invalid request method."
        }, status=400)
    except Exception as e:
        # Return error message if an exception occurs
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)

def discover_view(request):
    """Community discover page"""
    return render(request, 'community/discover.html')

@login_required
def like_post(request, post_id):
    try:
        # Get the post by its ID
        post = get_object_or_404(Post, id=post_id)

        # Toggle like status for the current user
        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user)
            liked = False
        else:
            post.liked_by.add(request.user)
            liked = True

        # Return like status and updated like count
        return JsonResponse({
            "success": True,
            "liked": liked,
            "likes_count": post.liked_by.count()
        })
    except Exception as e:
        # Return error message if an exception occurs
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)

@login_required
def collect_post(request, post_id):
    try:
        # Get the post by its ID
        post = get_object_or_404(Post, id=post_id)

        # Toggle collect status for the current user
        if post.collected_by.filter(id=request.user.id).exists():
            post.collected_by.remove(request.user)
            collected = False
        else:
            post.collected_by.add(request.user)
            collected = True

        # Return collect status and updated collect count
        return JsonResponse({
            "success": True,
            "collected": collected,
            "collections_count": post.collected_by.count()
        })
    except Exception as e:
        # Return error message if an exception occurs
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)

@csrf_exempt
def post_comment(request, post_id):
    try:
        # Get the post by its ID
        post = get_object_or_404(Post, id=post_id)

        if request.method == "GET":
            # Fetch all comments for the post
            comments = post.comments.all().order_by("-created_at")
            comment_data = [{
                "id": comment.id,
                "author": comment.author.nickname or comment.author.username,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M")
            } for comment in comments]

            # Return comment data in JSON format
            return JsonResponse({
                "success": True,
                "comments": comment_data
            })

        elif request.method == "POST":
            # Handle comment submission
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

            # Create a new comment and return its details in the response
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

        # Return error if request method is not GET or POST
        return JsonResponse({
            "success": False,
            "message": "Invalid request method."
        }, status=400)
    except Exception as e:
        # Return error message if an exception occurs
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)
