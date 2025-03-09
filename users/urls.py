from django.urls import path
from .views import register, user_login, user_logout, me_view, edit_profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('me/', me_view, name='me'),
    path("me/edit/", edit_profile, name="edit_profile"), 
]
