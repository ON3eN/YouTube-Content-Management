# workflow/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from chat.models import Message  # استدعاء موديل الرسائل

@login_required
def home_view(request):
    # في حال تم إرسال رسالة
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                content=content
            )
            return redirect('home')  # إعادة توجيه لتجنب تكرار الإرسال

    # جلب جميع الرسائل بترتيب زمني
    messages = Message.objects.order_by('timestamp')

    # تمرير الرسائل للقالب
    return render(request, 'workflow/home.html', {
        'messages': messages,
    })
