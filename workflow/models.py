from django.db import models
from django.contrib.auth.models import User

class الفيديو(models.Model):
    العنوان = models.CharField(max_length=255, verbose_name="عنوان الفيديو")
    وصف = models.TextField(blank=True, verbose_name="وصف الفيديو")
    الفيديو_الخام = models.FileField(upload_to='raw_videos/', verbose_name="الفيديو الخام")
    تاريخ_الرفع = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الرفع")

    المالك = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="صاحب الفيديو")

    def __str__(self):
        return self.العنوان

    class Meta:
        verbose_name = "فيديو"
        verbose_name_plural = "الفيديوهات"
