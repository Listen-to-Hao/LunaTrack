from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message', 'rating'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Please share your feedback', 'rows': 4}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Rate your experience (1-5)',
                'min': 1,
                'max': 5
            }),
        }