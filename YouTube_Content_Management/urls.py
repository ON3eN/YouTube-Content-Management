from django.contrib import admin
from django.urls import path, include  # تضمين include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # تطبيق الحسابات
    path('account/', include('account.urls')),

    # تطبيق خط الإنتاج
    path('workflow/', include('workflow.urls')),
]
