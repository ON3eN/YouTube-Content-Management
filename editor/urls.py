from django.urls import path
from . import views

app_name = 'editor'

urlpatterns = [
    path('tasks/', views.tasks_view, name='editor_tasks'),
    path('upload/', views.upload_video_view, name='editor_upload'),
    path('start-progress/<int:source_id>/', views.start_progress, name='start_progress'),
]
