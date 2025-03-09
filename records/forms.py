from django import forms
from .models import MenstrualRecord  # ✅ 确保只导入 MenstrualRecord

class MenstrualRecordForm(forms.ModelForm):
    SYMPTOM_CHOICES = [
        ('breast_tenderness', 'Breast Tenderness'),
        ('mood_swings', 'Mood Swings'),
        ('headache', 'Headache'),
        ('bloating', 'Bloating'),
        ('fatigue', 'Fatigue'),
        ('nausea', 'Nausea'),
        ('other', 'Other')
    ]

    pre_menstrual_symptoms = forms.MultipleChoiceField(
        choices=SYMPTOM_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
    menstrual_symptoms = forms.MultipleChoiceField(
        choices=SYMPTOM_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
    post_menstrual_symptoms = forms.MultipleChoiceField(
        choices=SYMPTOM_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = MenstrualRecord
        fields = ["start_date", "end_date", "blood_volume", "clotting",
                  "mood_swings", "stress_level", "pre_menstrual_symptoms",
                  "menstrual_symptoms", "post_menstrual_symptoms", "symptom_description"]

    def clean_pre_menstrual_symptoms(self):
        return self.cleaned_data["pre_menstrual_symptoms"] or []

    def clean_menstrual_symptoms(self):
        return self.cleaned_data["menstrual_symptoms"] or []

    def clean_post_menstrual_symptoms(self):
        return self.cleaned_data["post_menstrual_symptoms"] or []
