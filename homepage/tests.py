from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from homepage.models import Feedback

User = get_user_model()

class HomeViewTest(TestCase):
    def setUp(self):
        """Initialize test data"""
        self.client = Client()  # Initialize the test client
        self.user = User.objects.create_user(username="testuser", password="testpass")  # Create a test user
        self.feedback_url = reverse("home")  # URL for the 'home' view (corresponding to path('home/', home, name="home"))

    def test_home_page_loads(self):
        """Test if the GET request properly renders the form"""
        response = self.client.get(self.feedback_url)  # Send a GET request to the home page
        self.assertEqual(response.status_code, 200)  # Check that the response status code is 200 (OK)
        self.assertContains(response, '<form')  # Check if the HTML contains the form

    def test_submit_feedback_as_anonymous(self):
        """Test if an anonymous user can submit feedback"""
        response = self.client.post(self.feedback_url, {"content": "Great website!"})  # Submit feedback as anonymous
        self.assertEqual(response.status_code, 302)  # It should redirect to the homepage (302)
        self.assertEqual(Feedback.objects.count(), 1)  # Ensure that the feedback is saved in the database

    def test_submit_feedback_as_logged_in_user(self):
        """Test if a logged-in user can submit feedback"""
        self.client.login(username="testuser", password="testpass")  # Log in with the test user
        response = self.client.post(self.feedback_url, {"content": "Awesome site!"})  # Submit feedback while logged in
        self.assertEqual(response.status_code, 302)  # It should redirect to the homepage (302)
        feedback = Feedback.objects.first()  # Get the first feedback object in the database
        self.assertEqual(feedback.user, self.user)  # Ensure the feedback is correctly associated with the logged-in user

    def test_submit_empty_feedback(self):
        """Test if submitting empty feedback triggers form validation error"""
        response = self.client.post(self.feedback_url, {"content": ""})  # Submit empty feedback
        self.assertEqual(response.status_code, 200)  # The page should be returned without redirection (status 200)
        self.assertContains(response, "This field is required")  # Check for the error message on the form
        self.assertEqual(Feedback.objects.count(), 0)  # Ensure that no empty feedback is saved in the database
