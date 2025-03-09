from django.db import models
from django.conf import settings

class MenstrualRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")

    BLOOD_VOLUME_CHOICES = [('light', 'Light'), ('medium', 'Medium'), ('heavy', 'Heavy')]
    blood_volume = models.CharField(max_length=10, choices=BLOOD_VOLUME_CHOICES, verbose_name="Blood Volume", default='medium')

    CLOT_CHOICES = [('none', 'None'), ('small', 'Few Small Clots'), ('large', 'Many or Large Clots')]
    clotting = models.CharField(max_length=10, choices=CLOT_CHOICES, verbose_name="Clotting", default='none')

    MOOD_CHOICES = [('none', 'None'), ('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe')]
    mood_swings = models.CharField(max_length=10, choices=MOOD_CHOICES, verbose_name="Mood Swings", default='none')

    STRESS_LEVEL_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    stress_level = models.CharField(max_length=10, choices=STRESS_LEVEL_CHOICES, verbose_name="Stress Level", default='medium')

    SYMPTOM_CHOICES = [
        ('breast_tenderness', 'Breast Tenderness'),
        ('mood_swings', 'Mood Swings'),
        ('headache', 'Headache'),
        ('bloating', 'Bloating'),
        ('fatigue', 'Fatigue'),
        ('nausea', 'Nausea'),
        ('other', 'Other')
    ]

    pre_menstrual_symptoms = models.JSONField(default=list, blank=True, verbose_name="Pre-menstrual Symptoms")
    menstrual_symptoms = models.JSONField(default=list, blank=True, verbose_name="Menstrual Symptoms")
    post_menstrual_symptoms = models.JSONField(default=list, blank=True, verbose_name="Post-menstrual Symptoms")

    symptom_description = models.TextField(blank=True, verbose_name="Additional Symptoms")

    def __str__(self):
        return f"{self.user.username} - {self.start_date} to {self.end_date}"
