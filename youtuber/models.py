from django.db import models
from django.contrib.auth.models import User


class UploadedVideo(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_videos',       # يسهل: request.user.uploaded_videos.all()
        verbose_name="المستخدم"
    )

    title = models.CharField(
        max_length=200,
        verbose_name="اسم الفيديو"
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

    extras = models.TextField(
        blank=True,
        null=True,
        verbose_name="ملاحظات إضافية"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الرفع"
    )

    class Meta:
        verbose_name = "فيديو مرفوع"
        verbose_name_plural = "الفيديوهات المرفوعة"
        ordering = ['-uploaded_at']           # الأحدث أولًا
        indexes = [
            models.Index(fields=['user', '-uploaded_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    @property
    def safe_title(self):
        """عنوان بديل سريع إن احتجت عرضه عند غياب العنوان."""
        return self.title or self.file_name
