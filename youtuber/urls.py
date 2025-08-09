# youtuber/urls.py

from django.urls import path
from . import views

app_name = 'youtuber'

urlpatterns = [
    # ✅ صفحة عرض المهام (تتضمن نموذج رفع الفيديو وقائمة الفيديوهات)
    path('tasks/', views.tasks_view, name='youtuber_tasks'),

    # ✅ معالجة رفع الفيديو إلى Cloudinary
    path('upload/', views.upload_video_view, name='upload_video'),

    # ✅ حذف الفيديو من قاعدة البيانات وCloudinary
    path('delete/<int:video_id>/', views.delete_video_view, name='delete_video'),
]
