from django.contrib import admin
from .models import الفيديو

@admin.register(الفيديو)
class الفيديو_ادمن(admin.ModelAdmin):
    list_display = ('العنوان', 'المالك', 'تاريخ_الرفع')
    search_fields = ('العنوان', 'المالك__username')
    list_filter = ('تاريخ_الرفع',)
