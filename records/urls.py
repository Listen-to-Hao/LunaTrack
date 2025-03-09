from django.urls import path
from .views import record_list, add_record, edit_record, delete_record

urlpatterns = [
    path("", record_list, name="record"),
    path("add/", add_record, name="add_record"),
    path("<int:pk>/edit/", edit_record, name="edit_record"),
    path("<int:pk>/delete/", delete_record, name="delete_record"),
]
