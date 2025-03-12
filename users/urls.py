from django.urls import path
from .views import register, user_login, user_logout, me_view, edit_profile, delete_post, delete_comment, like_post, collect_post, post_comment, get_posts

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("me/", me_view, name="me"),
    path("me/edit/", edit_profile, name="edit_profile"),
    path("me/delete-post/<int:post_id>/", delete_post, name="delete_post"),
    path("me/delete-comment/<int:comment_id>/", delete_comment, name="delete_comment"),
    path('posts/<int:post_id>/like/', like_post, name='like_post'),
    path('posts/<int:post_id>/collect/', collect_post, name='collect_post'),
    path('posts/<int:post_id>/comment/', post_comment, name='post_comment'),
    path("me/posts/", get_posts, name="get_posts"),
]