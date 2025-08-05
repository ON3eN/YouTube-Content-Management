from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def tasks_view(request):
    return render(request, 'publisher/tasks.html')


@login_required
def publish_view(request):
    return render(request, 'publisher/publish.html')  # فيه أزرار تنزيل الفيديو والصورة
