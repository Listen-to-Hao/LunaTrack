from django.db import models
from django.conf import settings
from records.models import MenstrualRecord

class DummyAnalysisModel(models.Model):
    # Foreign key to UserProfile
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name="User", 
        related_name="dummy_analysis_records"
    )

    # Foreign key to MenstrualRecord
    record = models.ForeignKey(
        MenstrualRecord, 
        on_delete=models.CASCADE, 
        verbose_name="Menstrual Record", 
        related_name="dummy_analysis_records"
    )

    dummy_field = models.CharField(max_length=100, blank=True, verbose_name="Dummy Field")
    analysis_date = models.DateField(auto_now_add=True, verbose_name="Analysis Date")
    analysis_score = models.FloatField(default=0.0, verbose_name="Analysis Score")
    is_completed = models.BooleanField(default=False, verbose_name="Is Completed")

    ANALYSIS_TYPE_CHOICES = [
        ('basic', 'Basic Analysis'),
        ('advanced', 'Advanced Analysis'),
        ('custom', 'Custom Analysis'),
    ]
    analysis_type = models.CharField(
        max_length=20, 
        choices=ANALYSIS_TYPE_CHOICES, 
        default='basic', 
        verbose_name="Analysis Type"
    )

    notes = models.TextField(blank=True, verbose_name="Additional Notes")

    class Meta:
        managed = False  
        verbose_name = "Dummy Analysis Model"
        verbose_name_plural = "Dummy Analysis Models"
        ordering = ['-analysis_date'] 

    def __str__(self):
        return f"Dummy Analysis - {self.user.username} - {self.analysis_date}"