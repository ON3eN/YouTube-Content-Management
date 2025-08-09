from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cloudinary.uploader import upload as cloudinary_upload, destroy as cloudinary_destroy
from cloudinary.exceptions import Error as CloudinaryError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import UploadedVideo


@login_required
def tasks_view(request):
    uploaded_videos = UploadedVideo.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'youtuber/tasks.html', {
        'uploaded_videos': uploaded_videos
    })


@login_required
@require_POST
def upload_video_view(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video = request.FILES['video']
        title = request.POST.get('title', 'فيديو بدون اسم')
        extras = request.POST.get('extras', '')

        try:
            # رفع الفيديو إلى Cloudinary
            result = cloudinary_upload(
                video,
                resource_type='video',
                folder='youtuber_uploads/',
                use_filename=True,
                unique_filename=False
            )

            video_url = result.get('secure_url')
            public_id = result.get('public_id')

            if not video_url or not public_id:
                return JsonResponse({'success': False, 'error': 'فشل في الحصول على رابط الفيديو أو معرفه.'})

            # حفظ في قاعدة البيانات
            UploadedVideo.objects.create(
                user=request.user,
                title=title,
                video_url=video_url,
                file_name=video.name,
                extras=extras,
                public_id=public_id
            )

            return JsonResponse({'success': True})

        except (CloudinaryError, ValueError) as e:
            return JsonResponse({'success': False, 'error': f'خطأ أثناء رفع الفيديو: {str(e)}'})

    return JsonResponse({'success': False, 'error': 'الطلب غير صالح أو لا يحتوي على فيديو.'})


@require_POST
@login_required
def delete_video_view(request, video_id):
    video = get_object_or_404(UploadedVideo, id=video_id, user=request.user)

    try:
        if video.public_id:
            cloudinary_destroy(video.public_id, resource_type="video")

        video.delete()

        uploaded_videos = UploadedVideo.objects.filter(user=request.user).order_by('-uploaded_at')
        return render(request, 'youtuber/tasks.html', {
            'success': True,
            'uploaded_videos': uploaded_videos
        })

    except CloudinaryError as e:
        uploaded_videos = UploadedVideo.objects.filter(user=request.user).order_by('-uploaded_at')
        return render(request, 'youtuber/tasks.html', {
            'error': f"فشل في حذف الفيديو من Cloudinary: {str(e)}",
            'uploaded_videos': uploaded_videos
        })
