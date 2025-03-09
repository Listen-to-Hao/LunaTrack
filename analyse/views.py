from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def analyse_view(request):
    return render(request, 'analyse/analyse.html')  
