from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# استيراد login_view من تطبيق الحسابات
from account.views import login_view

urlpatterns = [
    # الصفحة الرئيسية توجه مباشرة لتسجيل الدخول
    path('', login_view, name='home'),

    # لوحة التحكم
    path('admin/', admin.site.urls),

    # مسارات تطبيق الحسابات
    path('account/', include('account.urls')),

    # مسارات تطبيق خط الإنتاج
    path('workflow/', include('workflow.urls')),
]

# دعم ملفات الوسائط (media) في بيئة التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
