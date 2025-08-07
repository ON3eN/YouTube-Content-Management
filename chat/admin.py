# chat/admin.py
from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'content', 'timestamp')
    search_fields = ('sender__username', 'content')

admin.site.register(Message, MessageAdmin)
