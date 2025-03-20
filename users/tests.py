from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse

class PostViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.post = Post.objects.create(author=self.user, content="Test post")
        self.comment = Comment.objects.create(post=self.post, author=self.user, content="Test comment")
    
    def test_get_posts(self):
        url = reverse('get_posts')  # Use the correct URL pattern name
        response = self.client.get(url, {"type": "created"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("posts", data)
        self.assertEqual(len(data["posts"]), 1)  # We have one post created by the user

    def test_like_post(self):
        url = reverse('like_post', args=[self.post.id])  # Use the correct URL pattern name
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["liked"])  # The user likes the post
        self.assertEqual(data["likes"], 1)  # Post's like count is 1

    def test_collect_post(self):
        url = reverse('collect_post', args=[self.post.id])  # Use the correct URL pattern name
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["collected"])  # The user collects the post
        self.assertEqual(data["collections"], 1)  # Post's collections count is 1

    def test_post_comment(self):
        url = reverse('post_comment', args=[self.post.id])  # Use the correct URL pattern name
        data = {"content": "New comment"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])  # Comment should be posted successfully
        self.assertEqual(data["comments_count"], 2)  # Post should have two comments

    def test_delete_post(self):
        url = reverse('delete_post', args=[self.post.id])  # Use the correct URL pattern name
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])  # Post should be deleted
        self.assertEqual(Post.objects.count(), 0)  # Post count should be 0

    def test_delete_comment(self):
        url = reverse('delete_comment', args=[self.comment.id])  # Use the correct URL pattern name
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])  # Comment should be deleted
        self.assertEqual(Comment.objects.count(), 0)  # Comment count should be 0

    def test_register_view(self):
        url = reverse('register')  # Use the correct URL pattern name
        data = {
            "username": "newuser",
            "password1": "password",
            "password2": "password"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration

    def test_login_view(self):
        url = reverse('user_login')  # Use the correct URL pattern name
        data = {
            "username": "testuser",
            "password": "password"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login

    def test_logout_view(self):
        url = reverse('user_logout')  # Use the correct URL pattern name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Should redirect after logout

    def test_edit_profile_view(self):
        url = reverse('edit_profile')  # Use the correct URL pattern name
        data = {
            "username": "updateduser",
            "password": "newpassword"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)  # Invalid request (since data is incomplete)
        
        # After correcting the form
        response = self.client.post(url, {"username": "updateduser", "first_name": "NewName"})
        self.assertEqual(response.status_code, 200)  # Successful profile update
        data = response.json()
        self.assertTrue(data["success"])  # Profile updated successfully

