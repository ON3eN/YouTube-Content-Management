from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ✅ استيراد صفحة الهوم من تطبيق workflow
from workflow.views import home_view

urlpatterns = [
    # ✅ الصفحة الرئيسية تفتح على home_view
    path('', home_view, name='home'),

    # لوحة تحكم Django
    path('admin/', admin.site.urls),

    # مسارات تطبيق الحسابات
    path('account/', include('account.urls')),

    # مسارات تطبيق خط الإنتاج (الواجهة الرئيسية)
    path('workflow/', include('workflow.urls')),

    # مسارات تطبيق اليوتيوبر
    path('youtuber/', include('youtuber.urls')),

    # مسارات بقية الفرق
    path('editor/', include('editor.urls')),
    path('thumbnailer/', include('thumbnailer.urls')),
    path('reviewer/', include('reviewer.urls')),
    path('publisher/', include('publisher.urls')),

    # تطبيق الدردشة الجماعية
    path('chat/', include('chat.urls')),
]

# دعم عرض الوسائط (Media) أثناء التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
