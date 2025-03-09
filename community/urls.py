from django.urls import path
from .views import discover_view, post_list, create_post, like_post, collect_post, add_comment

urlpatterns = [
    path('', discover_view, name='discover'),
    path('posts/', post_list, name='post_list'),  
    path('posts/create/', create_post, name='create_post'),
    path('posts/<int:post_id>/like/', like_post, name='like_post'),
    path('posts/<int:post_id>/collect/', collect_post, name='collect_post'),
    path('posts/<int:post_id>/comment/', add_comment, name='add_comment'),
]
