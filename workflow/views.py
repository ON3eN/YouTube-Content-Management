# workflow/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.apps import apps

from chat.models import Message


# ===== موديلات ديناميكية =====
def _get_video_model():
    """يرجّع موديل فيديو اليوتيوبر (UploadedVideo أو Video) داخل تطبيق youtuber."""
    return (
        apps.get_model('youtuber', 'UploadedVideo')
        or apps.get_model('youtuber', 'Video')
    )


def _get_workflow_video_model():
    """يرجّع موديل الفيديو داخل تطبيق workflow (الذي يحمل حالة_المونتاج)."""
    try:
        return apps.get_model('workflow', 'الفيديو')
    except Exception:
        return None


def _get_editor_rendered_model():
    """موديل مخرجات الممنتج (تمّ المونتاج) – قديم/بديل."""
    return apps.get_model('editor', 'EditorRendered')


def _get_editor_progress_model():
    """موديل تتبّع تقدّم الممنتج (جاري المونتاج) – قديم/بديل."""
    return apps.get_model('editor', 'EditorProgress')


# ===== أدوات جلب البيانات =====
def _get_videos_by_usernames(usernames):
    """
    يرجّع فيديوهات اليوتيوبر حسب أسماء المستخدمين.
    يدعم مفاتيح FK المحتملة: user / uploader / owner.
    """
    VideoModel = _get_video_model()
    if not VideoModel:
        return []

    qs = VideoModel.objects.all()
    field_names = {f.name for f in VideoModel._meta.get_fields()}

    fk_field = None
    for cand in ('user', 'uploader', 'owner'):
        if cand in field_names:
            fk_field = cand
            break

    if fk_field:
        qs = qs.filter(**{f'{fk_field}__username__in': usernames})

    qs = qs.order_by('-uploaded_at') if 'uploaded_at' in field_names else qs.order_by('-id')
    return qs


def _users_by_usernames(names):
    return User.objects.filter(username__in=names).order_by('username')


# ========= حالات المونتاج (المعتمدة الآن على workflow.الفيديو) =========
def _get_status_ids_from_workflow():
    """
    يحاول قراءة IDs للحالات من موديل workflow.الفيديو (الحالي).
    يرجّع: (edited_ids, in_progress_ids) كقوائم IDs للفيديو الأصلي (UploadedVideo)،
    وليس IDs سجلات workflow نفسها.
    """
    Model = _get_workflow_video_model()
    if not Model:
        return ([], [])

    fields = {f.name for f in Model._meta.get_fields()}
    if 'حالة_المونتاج' not in fields:
        return ([], [])

    # نحاول اكتشاف اسم الـ FK الذي يشير للفيديو الأصلي
    fk_candidates = ['source_video', 'video', 'youtuber_video', 'uploaded_video']
    fk_name = next((f for f in fk_candidates if f in fields), None)

    if fk_name:
        edited_ids = list(
            Model.objects.filter(حالة_المونتاج=2).values_list(f'{fk_name}_id', flat=True)
        )
        in_progress_ids = list(
            Model.objects.filter(حالة_المونتاج=1).values_list(f'{fk_name}_id', flat=True)
        )
    else:
        # لا يوجد FK واضح → نرجّع فاضي كي نستخدم الـ legacy
        return ([], [])

    # إزالة التكرارات للحفاظ على الأداء في القالب
    return (list(set(edited_ids)), list(set(in_progress_ids)))


# ========= باك أب قديم يعتمد على جداول editor =========
def _get_edited_ids_legacy():
    Model = _get_editor_rendered_model()
    if not Model:
        return []
    return list(set(Model.objects.values_list('source_video_id', flat=True)))


def _get_in_progress_ids_legacy():
    Progress = _get_editor_progress_model()
    if not Progress:
        return []
    return list(set(Progress.objects.values_list('source_video_id', flat=True)))


# ===== الصفحة الرئيسية =====
@login_required
def home_view(request):
    # استقبال رسالة دردشة
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, content=content)
            return redirect('home')

    # الرسائل بالترتيب الزمني
    messages = Message.objects.order_by('timestamp')

    # الأدوار مبنية على أسماء المستخدمين
    YOUTUBER_USERS     = ['youtuber']
    EDITOR_USERS       = ['montag']
    THUMBNAILER_USERS  = ['thumbnailer']
    REVIEWER_USERS     = ['reviewer']
    PUBLISHER_USERS    = ['nshr']

    # كل المستخدمين يشوفون فيديوهات اليوتيوبر
    youtuber_videos = _get_videos_by_usernames(YOUTUBER_USERS)

    # === حالات المونتاج ===
    # الأولوية لقراءة الحالة من workflow.الفيديو (الجديد) مع إرجاع IDs الفيديو الأصلي
    edited_ids, in_progress_ids = _get_status_ids_from_workflow()

    # إن لم نجد شيئًا (مثل مشروع قديم)، نستخدم الجداول القديمة في editor
    if not edited_ids and not in_progress_ids:
        edited_ids      = _get_edited_ids_legacy()       # تمّ المونتاج
        in_progress_ids = _get_in_progress_ids_legacy()  # جاري المونتاج

    # تمرير أسماء المستخدمين للأعمدة (اختياري)
    roles = {
        'youtuber':    {'label': 'يوتيوبر',        'users': _users_by_usernames(YOUTUBER_USERS)},
        'editor':      {'label': 'ممنتج',          'users': _users_by_usernames(EDITOR_USERS)},
        'thumbnailer': {'label': 'مصمم الثمنيل',   'users': _users_by_usernames(THUMBNAILER_USERS)},
        'reviewer':    {'label': 'مراجع',          'users': _users_by_usernames(REVIEWER_USERS)},
        'publisher':   {'label': 'مسؤول النشر',    'users': _users_by_usernames(PUBLISHER_USERS)},
    }

    # ملاحظة: قالب workflow/home.html يستخدم started_ids للاسم القديم
    # لذلك نمرّر alias لتجنّب تعديل القالب الآن.
    return render(
        request,
        'workflow/home.html',
        {
            'messages': messages,
            'youtuber_videos': youtuber_videos,
            'roles': roles,

            # في القالب:
            # - إذا id ضمن edited_ids       => تمّ المونتاج
            # - وإلا إذا ضمن started_ids    => جاري المونتاج
            # - غير ذلك                      => لم يتم المونتاج
            'edited_ids': edited_ids,
            'in_progress_ids': in_progress_ids,
            'started_ids': in_progress_ids,  # alias ليتوافق مع القالب الحالي
        },
    )
