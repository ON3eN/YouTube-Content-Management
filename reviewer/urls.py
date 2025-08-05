from django.urls import path
from . import views

app_name = 'reviewer'

urlpatterns = [
    path('tasks/', views.tasks_view, name='reviewer_tasks'),
]
