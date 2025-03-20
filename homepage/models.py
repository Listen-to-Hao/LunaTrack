from django.db import models
from django.conf import settings

class Feedback(models.Model):
    # ForeignKey to User model (optional)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Link to the user model
        on_delete=models.SET_NULL,  # Set to NULL if the user is deleted
        null=True,  
        blank=True,  
        verbose_name="User"  # Label for this field
    )

    # The user's name (in case the feedback is anonymous)
    name = models.CharField(max_length=100, verbose_name="Your Name")  

    # The user's email address
    email = models.EmailField(verbose_name="Your Email")

    # The main feedback message or content
    message = models.TextField(verbose_name="Your Feedback")

    # Rating of the feedback, optional and ranging from 1 to 5
    rating = models.PositiveIntegerField(  
        verbose_name="Rating",  # Label for this field
        null=True,  # Allow null values
        blank=True,  # Allow blank values
        help_text="Rate your experience (1-5)"  # Hint for the user
    )

    # Timestamp for when the feedback was created
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submission Time")

    def __str__(self):
        # Return a string representation of the feedback
        if self.user:
            return f"Feedback from {self.user.username} (Rating: {self.rating})"
        return f"Feedback from {self.name} (Rating: {self.rating})"

    class Meta:
        # Custom verbose names for the model in the admin interface
        verbose_name = "User Feedback"
        verbose_name_plural = "User Feedbacks"
