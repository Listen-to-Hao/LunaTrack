from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nickname", default="Mysterious User")  
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.jpg", blank=True, null=True)
    email = models.EmailField(unique=True)

    height = models.FloatField(blank=True, null=True, verbose_name="Height (cm)")

    AGE_GROUPS = [
        ("teen", "Teenager (13-19)"),
        ("young_adult", "Young Adult (20-35)"),
        ("middle_aged", "Middle-Aged (36-55)"),
        ("senior", "Senior (56+)"),
    ]
    age_group = models.CharField(max_length=15, choices=AGE_GROUPS, blank=True, null=True, verbose_name="Age Group")

    # 点赞的帖子
    liked_posts = models.ManyToManyField("community.Post", related_name="liked_by", blank=True)
    # 收藏的帖子
    collected_posts = models.ManyToManyField("community.Post", related_name="collected_by", blank=True)

    def __str__(self):
        return self.nickname if self.nickname else self.username