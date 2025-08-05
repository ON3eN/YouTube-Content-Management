from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage


@login_required
def tasks_view(request):
    return render(request, 'thumbnailer/tasks.html')


@login_required
def upload_thumbnail_view(request):
    if request.method == 'POST' and request.FILES.get('thumbnail'):
        thumbnail = request.FILES['thumbnail']
        fs = FileSystemStorage()
        filename = fs.save(thumbnail.name, thumbnail)

        return render(request, 'thumbnailer/upload.html', {
            'success': True,
            'filename': filename
        })

    return render(request, 'thumbnailer/upload.html')
