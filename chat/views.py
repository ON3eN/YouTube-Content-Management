# chat/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def chat_view(request):
    """
    عرض واجهة الدردشة الجماعية وإرسال الرسائل.
    """
    if request.method == 'POST':
        النص = request.POST.get('نص', '').strip()
        if النص:
            Message.objects.create(
                sender=request.user,
                content=النص,
                is_reply=False
            )
        return redirect(request.META.get('HTTP_REFERER', 'chat:chat_home'))

    messages = Message.objects.order_by('timestamp')
    return render(request, 'chat/chat.html', {
        'messages': messages,
    })
