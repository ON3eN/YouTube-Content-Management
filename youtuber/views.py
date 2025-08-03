# youtuber/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

@login_required
def tasks_view(request):
    return render(request, 'youtuber/tasks.html')


@login_required
def upload_video_view(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video = request.FILES['video']
        fs = FileSystemStorage()
        fs.save(video.name, video)
        return render(request, 'youtuber/upload.html', {
            'success': True,
            'filename': video.name
        })
    
    return render(request, 'youtuber/upload.html')
