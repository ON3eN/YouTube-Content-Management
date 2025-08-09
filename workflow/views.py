# workflow/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.apps import apps

from chat.models import Message


# ----- مساعد: احصل موديل الفيديو -----
def _get_video_model():
    """
    يرجّع موديل الفيديو من تطبيق youtuber (UploadedVideo أو Video).
    """
    return (
        apps.get_model('youtuber', 'UploadedVideo')
        or apps.get_model('youtuber', 'Video')
    )


# ----- مساعد: فيديوهات بحسب أسماء مستخدمين -----
def _get_videos_by_usernames(usernames):
    """
    يرجّع فيديوهات رُفعت بواسطة مجموعة أسماء مستخدمين محدّدة.
    يعمل سواء كان الحقل ForeignKey اسمه: user / uploader / owner.
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
        # فلترة على username
        qs = qs.filter(**{f'{fk_field}__username__in': usernames})

    # ترتيب منطقي
    if 'uploaded_at' in field_names:
        qs = qs.order_by('-uploaded_at')
    else:
        qs = qs.order_by('-id')

    return qs


# ----- مساعد: جلب مستخدمين بالاسماء (لإظهارهم في الأعمدة) -----
def _users_by_usernames(names):
    return User.objects.filter(username__in=names).order_by('username')


@login_required
def home_view(request):
    # استقبال رسالة دردشة جديدة
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, content=content)
            return redirect('home')

    # جميع الرسائل زمنياً
    messages = Message.objects.order_by('timestamp')

    # أسماء المستخدمين المعتمدة لكل دور
    YOUTUBER_USERS     = ['youtuber']
    EDITOR_USERS       = ['montag']         # الممنتج
    THUMBNAILER_USERS  = ['thumbnailer']    # مصمم الثمنيل
    REVIEWER_USERS     = ['reviewer']       # المراجع
    PUBLISHER_USERS    = ['nshr']           # مسؤول النشر

    # كل المستخدمين يشوفون فيديوهات اليوتيوبر (حسب اسم المستخدم، مو حسب الوظيفة)
    youtuber_videos = _get_videos_by_usernames(YOUTUBER_USERS)

    # لو تحتاج تعرض أسماء أصحاب الأعمدة في الواجهة:
    roles = {
        'youtuber':    {'label': 'يوتيوبر',        'users': _users_by_usernames(YOUTUBER_USERS)},
        'editor':      {'label': 'ممنتج',          'users': _users_by_usernames(EDITOR_USERS)},
        'thumbnailer': {'label': 'مصمم الثمنيل',   'users': _users_by_usernames(THUMBNAILER_USERS)},
        'reviewer':    {'label': 'مراجع',          'users': _users_by_usernames(REVIEWER_USERS)},
        'publisher':   {'label': 'مسؤول النشر',    'users': _users_by_usernames(PUBLISHER_USERS)},
    }

    return render(
        request,
        'workflow/home.html',
        {
            'messages': messages,
            'youtuber_videos': youtuber_videos,  # الفيديوهات تُعرض للجميع
            'roles': roles,                      # لو حبيت تستخدمها في القالب
        },
    )
