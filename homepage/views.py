from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback

def home(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after submission
    else:
        form = FeedbackForm()

    return render(request, 'homepage/home.html', {'form': form})