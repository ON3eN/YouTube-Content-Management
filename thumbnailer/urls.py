from django.urls import path
from . import views

app_name = 'thumbnailer'

urlpatterns = [
    path('tasks/', views.tasks_view, name='thumbnailer_tasks'),
]
