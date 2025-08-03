from django.contrib import admin
from .models import الملف_الشخصي

@admin.register(الملف_الشخصي)
class الملف_الشخصي_ادمن(admin.ModelAdmin):
    list_display = ('المستخدم', 'الوظيفة')
    list_filter = ('الوظيفة',)
    search_fields = ('المستخدم__username', 'المستخدم__email')
