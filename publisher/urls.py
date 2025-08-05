from django.urls import path
from . import views

app_name = 'publisher'

urlpatterns = [
    path('tasks/', views.tasks_view, name='publisher_tasks'),
]
