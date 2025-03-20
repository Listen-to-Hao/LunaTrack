from django.http import JsonResponse
from django.shortcuts import render
from .forms import FeedbackForm
from .models import Feedback

def home(request):
    if request.method == 'POST':  # If the request is a POST (form submission)
        form = FeedbackForm(request.POST)  # Create a form instance with POST data
        if form.is_valid():  # Check if the form is valid
            try:
                feedback = form.save(commit=False)  # Save the form data without committing to the database yet
                # If the user is authenticated, associate the feedback with the logged-in user
                if request.user.is_authenticated:
                    feedback.user = request.user
                feedback.save()  # Save the feedback instance to the database
                return JsonResponse({"success": True})  # Return a JSON response indicating success
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)}, status=500)  # Return error if saving feedback fails
        else:
            # If form validation fails, return a JSON response with the errors
            errors = form.errors.as_json()  # Convert errors to JSON format
            return JsonResponse({"success": False, "error": errors}, status=400)  # Return the errors in a JSON response
    else:
        form = FeedbackForm()  # If the request is GET, create an empty form

    return render(request, 'homepage/home.html', {'form': form})  # Render the homepage with the form