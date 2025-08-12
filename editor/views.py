# editor/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.apps import apps
from django.db import transaction
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

import cloudinary.uploader

from .models import EditorRendered, EditorProgress


# ---------- مساعد: الحصول على موديل فيديوهات اليوتيوبر ----------
def _get_youtuber_video_model():
    """
    يرجّع موديل فيديوهات اليوتيوبر: UploadedVideo أو Video إن وجد.
    """
    return (
        apps.get_model("youtuber", "UploadedVideo")
        or apps.get_model("youtuber", "Video")
    )


def _youtuber_videos_qs():
    """
    يرجّع فيديوهات اليوتيوبر (حساب username='youtuber').
    يدعم أسماء الحقول: user / uploader / owner.
    يرتبها بالأحدث.
    """
    VideoModel = _get_youtuber_video_model()
    if not VideoModel:
        return []

    qs = VideoModel.objects.all()
    fields = {f.name for f in VideoModel._meta.get_fields()}

    # نكتشف اسم حقل الـ FK
    fk = None
    for cand in ("user", "uploader", "owner"):
        if cand in fields:
            fk = cand
            break

    if fk:
        qs = qs.filter(**{f"{fk}__username": "youtuber"})

    qs = qs.order_by("-uploaded_at") if "uploaded_at" in fields else qs.order_by("-id")
    return qs


# ---------- صفحة مهام الممنتج ----------
@login_required
@require_http_methods(["GET", "POST"])
@csrf_protect
def tasks_view(request):
    """
    GET  -> يعرض صفحة الممنتج:
            - فيديوهات اليوتيوبر (مع استثناء ما رُفع للمراجعة).
            - بطاقة "حالة المراجعة" من EditorRendered.
    POST -> يرفع فيديو الممنتج إلى Cloudinary، وينشئ سجل EditorRendered بالحالة pending.
    المتوقّع من الواجهة: إرسال video + source_video_id.
    """
    VideoModel = _get_youtuber_video_model()
    if not VideoModel:
        # في حال عدم وجود موديل اليوتيوبر، نظهر الصفحة فارغة
        return render(
            request,
            "editor/tasks.html",
            {"youtuber_videos": [], "review_items": []},
        )

    if request.method == "POST":
        file_obj = request.FILES.get("video")
        source_id = request.POST.get("source_video_id")

        if not source_id:
            return JsonResponse(
                {"success": False, "error": "يرجى اختيار الفيديو الأصلي."},
                status=400,
            )

        if not file_obj:
            return JsonResponse(
                {"success": False, "error": "يرجى اختيار ملف فيديو."},
                status=400,
            )

        try:
            source_video = VideoModel.objects.get(pk=source_id)
        except VideoModel.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "الفيديو الأصلي غير موجود."},
                status=404,
            )

        try:
            # رفع إلى Cloudinary (مجلد editor_upload)
            up_res = cloudinary.uploader.upload(
                file_obj,
                resource_type="video",
                folder="editor_upload",
                overwrite=False,
            )
            secure_url = up_res.get("secure_url")
            public_id = up_res.get("public_id")

            if not secure_url or not public_id:
                return JsonResponse(
                    {"success": False, "error": "فشل الرفع إلى Cloudinary."},
                    status=500,
                )

            # تحديد عنوان مناسب لسجل الممنتج
            src_title = getattr(source_video, "title", None) or getattr(source_video, "العنوان", None)
            title = src_title or getattr(file_obj, "name", "rendered.mp4")

            # إنشاء سجل الممنتج بالحالة pending
            with transaction.atomic():
                EditorRendered.objects.create(
                    user=request.user,
                    source_video=source_video,
                    title=title,
                    video_url=secure_url,
                    public_id=public_id,
                    file_name=getattr(file_obj, "name", "rendered.mp4"),
                    status=EditorRendered.ReviewStatus.PENDING,
                )

            return JsonResponse(
                {"success": True, "url": secure_url, "public_id": public_id}
            )

        except Exception as e:
            return JsonResponse(
                {"success": False, "error": f"خطأ أثناء الرفع: {e}"},
                status=500,
            )

    # ===== GET =====
    # IDs للفيديوهات التي تم إرسالها للمراجعة كي نستثنيها من قائمة اليوتيوبر
    sent_ids = list(
        EditorRendered.objects.filter(source_video__isnull=False)
        .values_list("source_video_id", flat=True)
        .distinct()
    )

    # فيديوهات اليوتيوبر المتاحة (غير المرسلة للمراجعة)
    youtuber_videos_qs = _youtuber_videos_qs()
    if hasattr(youtuber_videos_qs, "exclude"):
        youtuber_videos = youtuber_videos_qs.exclude(id__in=sent_ids)
    else:
        youtuber_videos = []

    # عناصر حالة المراجعة (تحت المراجعة/مؤكد/مرفوض)
    review_items = (
        EditorRendered.objects.select_related("source_video", "user")
        .order_by("-uploaded_at")
    )

    return render(
        request,
        "editor/tasks.html",
        {
            "youtuber_videos": youtuber_videos,
            "review_items": review_items,
        },
    )


# ---------- رفع بديل (اختياري) ----------
@login_required
def upload_video_view(request):
    """
    مسار بديل بسيط لو احتجت رفع من صفحة ثانية (ليس من tasks).
    يرفع للفولدر editor_upload ويرجع JSON.
    """
    if request.method == "POST" and request.FILES.get("video"):
        file_obj = request.FILES["video"]
        try:
            up_res = cloudinary.uploader.upload(
                file_obj,
                resource_type="video",
                folder="editor_upload",
                overwrite=False,
            )
            return JsonResponse(
                {
                    "success": True,
                    "url": up_res.get("secure_url"),
                    "public_id": up_res.get("public_id"),
                }
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return HttpResponseBadRequest("استخدم POST مع حقل video.")


# ---------- تسجيل “جاري المونتاج” عند الضغط على زر تنزيل ----------
@require_POST
@login_required
def start_progress(request, vid_id):
    """
    تُستدعى عبر AJAX عند ضغط الممنتج زر "تنزيل" للفيديو الأصلي.
    تنشئ/تثبت وجود سجل EditorProgress لتظهر الحالة 'جاري المونتاج' في الصفحة الرئيسية.
    """
    try:
        EditorProgress.objects.get_or_create(
            user=request.user,
            source_video_id=vid_id,
            defaults={"started_at": timezone.now()},
        )
        return JsonResponse({"ok": True})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)
