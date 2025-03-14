from django.db import models
from users.models import UserProfile
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="created_posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)  
    
    def __str__(self):
        return f"Post by {self.author.username} on {self.created_at}"

    # 点赞和收藏的计数（通过反向查询集）
    @property
    def likes_count(self):
        return self.liked_by.count()

    @property
    def collections_count(self):
        return self.collected_by.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(verbose_name="Comment Content")

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.id} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"