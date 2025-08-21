# editor/urls.py
from django.urls import path
from . import views

app_name = 'editor'

urlpatterns = [
    # صفحة مهام الممنتج (عرض فيديوهات اليوتيوبر + رفع الفيديو المُمنتج + قائمة المراجعة)
    path('tasks/', views.tasks_view, name='editor_tasks'),

    # مسار رفع بديل (اختياري)
    path('upload/', views.upload_video_view, name='editor_upload'),

    # API: تسجيل بدء المونتاج عند الضغط على زر "تنزيل"
    # ملاحظة: يجب أن يطابق اسم البراميتر توقيع الدالة: start_progress(request, source_id)
    path('start-progress/<int:source_id>/', views.start_progress, name='start_progress'),
]
