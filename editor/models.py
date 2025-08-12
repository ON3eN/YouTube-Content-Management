# editor/models.py
from django.db import models
from django.contrib.auth.models import User


class EditorRendered(models.Model):
    """
    يمثل الفيديو النهائي بعد المونتاج والذي يرفعه الممنتج إلى Cloudinary.
    يحتوي كذلك على حالة المراجعة (تحت المراجعة/مؤكد/مرفوض) وملاحظة المراجع.
    """

    class ReviewStatus(models.TextChoices):
        PENDING   = "pending",   "تحت المراجعة"
        CONFIRMED = "confirmed", "مؤكد"
        REJECTED  = "rejected",  "مرفوض"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="الممنتج",
        null=True,          # تُركت مؤقتًا لتفادي مشاكل البيانات القديمة
        blank=True,
    )

    # الفيديو الأصلي القادم من اليوتيوبر
    source_video = models.ForeignKey(
        "youtuber.UploadedVideo",          # ربط نصّي لتفادي الاستيراد الدائري
        on_delete=models.SET_NULL,         # لو انحذف الأصلي نخليها NULL
        null=True,
        blank=True,
        related_name="renders",
        verbose_name="الفيديو الأصلي (من اليوتيوبر)"
    )

    title = models.CharField(
        max_length=200,
        verbose_name="اسم الفيديو المُمنتج"
    )

    video_url = models.URLField(
        verbose_name="رابط الفيديو على Cloudinary"
    )

    public_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="معرف Cloudinary"
    )

    file_name = models.CharField(
        max_length=255,
        verbose_name="اسم الملف"
    )

    # ملاحظات عامة من الممنتج (إن وُجدت)
    extras = models.TextField(
        blank=True,
        null=True,
        verbose_name="ملاحظات"
    )

    # ===== حالة المراجعة =====
    status = models.CharField(
        max_length=10,
        choices=ReviewStatus.choices,
        default=ReviewStatus.PENDING,
        db_index=True,
        verbose_name="حالة المراجعة"
    )

    review_note = models.TextField(
        blank=True,
        null=True,
        verbose_name="ملاحظة المراجع"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الرفع"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تعديل"
    )

    class Meta:
        verbose_name = "فيديو مُمنتج"
        verbose_name_plural = "الفيديوهات المُمنتجة"
        ordering = ("-uploaded_at",)
        indexes = [
            models.Index(fields=["user", "-uploaded_at"], name="editor_edit_user_id_d7d6e3_idx"),
            models.Index(fields=["status", "-uploaded_at"], name="editor_status_idx"),
            models.Index(fields=["source_video", "-uploaded_at"], name="editor_source_idx"),
        ]

    # ======== دوال مساعدة لسهولة التغيير من الفيوز ========
    def mark_pending(self, note: str | None = None):
        self.status = self.ReviewStatus.PENDING
        if note is not None:
            self.review_note = note
        self.save(update_fields=["status", "review_note", "updated_at"])

    def confirm(self):
        self.status = self.ReviewStatus.CONFIRMED
        # عند التأكيد، لا حاجة للاحتفاظ بملاحظة رفض سابقة
        self.review_note = None
        self.save(update_fields=["status", "review_note", "updated_at"])

    def reject(self, note: str | None = None):
        self.status = self.ReviewStatus.REJECTED
        if note is not None:
            self.review_note = note
        self.save(update_fields=["status", "review_note", "updated_at"])

    # مفيد للقالب (CSS class)
    @property
    def status_css(self) -> str:
        return self.status  # pending / confirmed / rejected

    def __str__(self):
        base = self.title or self.file_name or "Rendered"
        owner = f" by {self.user.username}" if self.user_id else ""
        st = dict(self.ReviewStatus.choices).get(self.status, self.status)
        return f"{base}{owner} [{st}]"


class EditorProgress(models.Model):
    """
    يسجل أن الممنتج بدأ العمل على فيديو معين (بمجرد الضغط على زر تنزيل).
    نستعمله لإظهار حالة 'جاري المونتاج' في الصفحة الرئيسية.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="الممنتج الذي بدأ العمل"
    )

    source_video = models.ForeignKey(
        "youtuber.UploadedVideo",
        on_delete=models.CASCADE,
        related_name="edit_progress",
        verbose_name="الفيديو الأصلي"
    )

    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ البدء"
    )

    class Meta:
        verbose_name = "بدء مونتاج"
        verbose_name_plural = "بدء المونتاج"
        # لا نسمح إلا بسجل واحد لكل فيديو أصلي (أول بداية تكفي لاعتبار الحالة 'جاري')
        unique_together = (("source_video",),)
        indexes = [
            models.Index(fields=["-started_at"]),
        ]

    def __str__(self):
        who = self.user.username if self.user_id else "unknown"
        return f"Progress for {self.source_video_id} by {who}"
