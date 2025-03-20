from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from community.models import Post, Comment

User = get_user_model()

class CommunityViewsTest(TestCase):
    def setUp(self):
        """Initialize test data"""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user2 = User.objects.create_user(username="testuser2", password="testpass")
        self.post = Post.objects.create(author=self.user, content="Test Post")

    def test_post_list(self):
        """Test the post list API"""
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertIn("posts", response.json())

    def test_create_post(self):
        """Test the create post API"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("create_post"), {
            "content": "New Test Post",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(Post.objects.count(), 2)

    def test_create_post_empty_content(self):
        """Test creating a post with empty content (should return 400 error)"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("create_post"), {"content": ""})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])

    def test_like_post(self):
        """Test the like and unlike post API"""
        self.client.login(username="testuser", password="testpass")

        response = self.client.post(reverse("like_post", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["liked"])
        self.assertEqual(self.post.liked_by.count(), 1)

        response = self.client.post(reverse("like_post", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["liked"])
        self.assertEqual(self.post.liked_by.count(), 0)

    def test_collect_post(self):
        """Test the collect and uncollect post API"""
        self.client.login(username="testuser", password="testpass")

        response = self.client.post(reverse("collect_post", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["collected"])
        self.assertEqual(self.post.collected_by.count(), 1)

        response = self.client.post(reverse("collect_post", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["collected"])
        self.assertEqual(self.post.collected_by.count(), 0)

    def test_get_comments(self):
        """Test the get post comments API"""
        Comment.objects.create(post=self.post, author=self.user, content="Nice post!")
        response = self.client.get(reverse("post_comment", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(len(response.json()["comments"]), 1)

    def test_post_comment(self):
        """Test the post comment API"""
        self.client.login(username="testuser", password="testpass")

        response = self.client.post(reverse("post_comment", args=[self.post.id]), {
            "content": "Great Post!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(self.post.comments.count(), 1)

    def test_post_comment_empty(self):
        """Test posting an empty comment (should return 400 error)"""
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("post_comment", args=[self.post.id]), {
            "content": ""
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
