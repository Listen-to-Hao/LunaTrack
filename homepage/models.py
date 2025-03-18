from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name="Your Name")
    email = models.EmailField(verbose_name="Your Email")
    message = models.TextField(verbose_name="Your Feedback")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submission Time")

    def __str__(self):
        return f"Feedback from {self.name}"

    class Meta:
        verbose_name = "User Feedback"
        verbose_name_plural = "User Feedbacks"