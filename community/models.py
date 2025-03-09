from django.db import models
from users.models import UserProfile
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField(verbose_name="Post Content") 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    images = models.ImageField(upload_to="post_images/", blank=True, null=True, verbose_name="Images")
    
    likes = models.ManyToManyField(UserProfile, related_name="liked_posts_set", blank=True)
    collections = models.ManyToManyField(UserProfile, related_name="collected_posts_set", blank=True)

    def __str__(self):
        return f"Post by {self.author.username} on {self.created_at}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(verbose_name="Comment Content")

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.id} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
