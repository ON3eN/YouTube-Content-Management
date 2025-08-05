from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# استيراد صفحة تسجيل الدخول لربطها بالصفحة الرئيسية
from account.views import login_view

urlpatterns = [
    # جعل الصفحة الرئيسية تفتح صفحة تسجيل الدخول
    path('', login_view, name='home'),

    # لوحة تحكم Django
    path('admin/', admin.site.urls),

    # مسارات تطبيق الحسابات
    path('account/', include('account.urls')),

    # مسارات تطبيق خط الإنتاج
    path('workflow/', include('workflow.urls')),

    # مسارات تطبيق اليوتيوبر
    path('youtuber/', include('youtuber.urls')),

    # ✅ مسارات التطبيقات الجديدة
    path('editor/', include('editor.urls')),
    path('thumbnailer/', include('thumbnailer.urls')),
    path('reviewer/', include('reviewer.urls')),
    path('publisher/', include('publisher.urls')),
]

# دعم ملفات الوسائط (Media) في وضع التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
