from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class الفيديو(models.Model):
    العنوان = models.CharField(max_length=255, verbose_name="عنوان الفيديو")
    وصف = models.TextField(blank=True, verbose_name="وصف الفيديو")
    الفيديو_الخام = models.FileField(upload_to='raw_videos/', verbose_name="الفيديو الخام")
    تاريخ_الرفع = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الرفع")
    المالك = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="صاحب الفيديو")

    # ▼▼ حقول سير عمل المونتاج (جديدة) ▼▼
    حالة_المونتاج_اختيارات = (
        (0, "لم يتم المونتاج"),
        (1, "جاري المونتاج"),
        (2, "تم المونتاج"),
    )
    حالة_المونتاج = models.PositiveSmallIntegerField(
        choices=حالة_المونتاج_اختيارات, default=0, db_index=True, verbose_name="حالة المونتاج"
    )
    تاريخ_بدء_المونتاج = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ بدء المونتاج")
    تاريخ_انتهاء_المونتاج = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ انتهاء المونتاج")

    # دوال مساعدة آمنة لتغيير الحالة من الفيوز
    def ابدأ_المونتاج(self, force=False):
        """
        وسم الفيديو بأنه (جاري المونتاج).
        إذا كان منتهي وتم استدعاؤها، لن تغيّر الحالة إلا لو force=True.
        """
        if self.H_هي_تم_المونتاج() and not force:
            return
        self.حالة_المونتاج = 1
        if not self.تاريخ_بدء_المونتاج:
            self.تاريخ_بدء_المونتاج = timezone.now()
        self.save(update_fields=["حالة_المونتاج", "تاريخ_بدء_المونتاج"])

    def انهي_المونتاج(self):
        """وسم الفيديو بأنه (تم المونتاج)."""
        self.حالة_المونتاج = 2
        self.تاريخ_انتهاء_المونتاج = timezone.now()
        self.save(update_fields=["حالة_المونتاج", "تاريخ_انتهاء_المونتاج"])

    # خصائص مريحة للقراءة في القوالب
    def H_هي_قيد_المونتاج(self):
        return self.حالة_المونتاج == 1

    def H_هي_تم_المونتاج(self):
        return self.حالة_المونتاج == 2

    def __str__(self):
        return self.العنوان

    class Meta:
        verbose_name = "فيديو"
        verbose_name_plural = "الفيديوهات"
