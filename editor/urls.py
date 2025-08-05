from django.urls import path
from . import views

app_name = 'editor'

urlpatterns = [
    path('tasks/', views.tasks_view, name='editor_tasks'),
]
