from django.urls import path
from .views import analyse_view

urlpatterns = [
    path('', analyse_view, name='analyse'), 
]
