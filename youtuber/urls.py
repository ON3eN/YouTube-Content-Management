from django.urls import path
from . import views

app_name = 'youtuber'

urlpatterns = [
    path('tasks/', views.tasks_view, name='youtuber_tasks'),  # <-- اسم واضح ومتطابق مع الهيدر
]
