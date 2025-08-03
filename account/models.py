from django.db import models
from django.contrib.auth.models import User

class الملف_الشخصي(models.Model):
    المستخدم = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="المستخدم"
    )

    خيارات_الوظائف = [
        ('youtuber', 'يوتيوبر'),
        ('editor', 'ممنتج'),
        ('thumbnailer', 'مصمم الثمنيل'),
        ('reviewer', 'مراجع'),
        ('publisher', 'مسؤول نشر'),
        ('manager', 'مدير'),
    ]

    الوظيفة = models.CharField(
        max_length=20,
        choices=خيارات_الوظائف,
        verbose_name="الوظيفة"
    )

    def __str__(self):
        return f"{self.المستخدم.username} - {self.get_الوظيفة_display()}"

    class Meta:
        verbose_name = "الملف الشخصي"
        verbose_name_plural = "الملفات الشخصية"
