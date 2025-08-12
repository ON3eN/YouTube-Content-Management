"""
إعدادات مشروع YouTube_Content_Management (Django 5.x)
"""

from pathlib import Path
import os
import cloudinary  # ربط إعدادات كلاوديناري

# ===== المسارات الأساسية =====
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== الأمان (لا تستخدم هذه القيم في الإنتاج) =====
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-secret")
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# ===== التطبيقات =====
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # طرف ثالث
    "cloudinary",
    "cloudinary_storage",

    # تطبيقاتك
    "account",
    "workflow",
    "youtuber",
    "editor",
    "thumbnailer",
    "reviewer",
    "publisher",
    "chat",
]

# ===== الوسطاء =====
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ===== URLs / Templates =====
ROOT_URLCONF = "YouTube_Content_Management.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "YouTube_Content_Management.wsgi.application"

# ===== قاعدة البيانات (SQLite للتطوير) =====
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ===== التحقق من كلمات المرور =====
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ===== اللغة والمنطقة =====
LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Riyadh"
USE_I18N = True
USE_TZ = True
# USE_L10N أُزيلت في Django 5

# ===== الملفات الثابتة والإعلامية =====
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ===== إعدادات Cloudinary =====
# اسحب من المتغيّرات أو استخدم القيم الحالية للتجارب المحلية
CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "dehrixr6p")
API_KEY = os.getenv("CLOUDINARY_API_KEY", "315721475167312")
API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "Oe6tSRcilo2WYbkg_7FhELh--bM")

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": CLOUD_NAME,
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
}

# تهيئة مكتبة cloudinary (مهم)
cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET,
)

# اجعل Cloudinary هو مخزن الوسائط الافتراضي (Media)
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# مجلدات رفع افتراضية (نستخدمها في الـ views)
CLOUDINARY_YOUTUBER_FOLDER = os.getenv("CLOUDINARY_YOUTUBER_FOLDER", "youtuber_upload")
CLOUDINARY_EDITOR_FOLDER   = os.getenv("CLOUDINARY_EDITOR_FOLDER", "editor_upload")

# ===== إعدادات أخرى =====
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "/account/login/"
