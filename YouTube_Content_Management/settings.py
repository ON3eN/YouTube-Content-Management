"""
إعدادات مشروع YouTube_Content_Management باستخدام Django 5.2.4
https://docs.djangoproject.com/en/5.2/topics/settings/
"""

from pathlib import Path
import cloudinary  # ← استدعاء مكتبة Cloudinary لربط الإعدادات

# المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# مفتاح الأمان (يجب تغييره في الإنتاج)
SECRET_KEY = 'django-insecure-5+=6#o*dtt^@zha^iyo58f=9tq6_d&!f82i=7syv^guqz2@tox'

# وضع التطوير
DEBUG = True

# العناوين المسموح بها
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # تطبيقات خارجية
    'cloudinary',
    'cloudinary_storage',

    # تطبيقات مخصصة
    'account',
    'workflow',
    'youtuber',
    'editor',
    'thumbnailer',
    'reviewer',
    'publisher',
    'chat',
]

# الوسطاء
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ملف URL الرئيسي
ROOT_URLCONF = 'YouTube_Content_Management.urls'

# إعدادات القوالب
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'YouTube_Content_Management.wsgi.application'

# قاعدة البيانات
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# تحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# اللغة والمنطقة
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# الملفات الثابتة
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ملفات الوسائط (الميديا)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# إعدادات Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dehrixr6p',
    'API_KEY': '315721475167312',
    'API_SECRET': 'Oe6tSRcilo2WYbkg_7FhELh--bM',
}

# ربط إعدادات Cloudinary يدويًا ← ضروري عشان يشتغل بدون أخطاء
cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=CLOUDINARY_STORAGE['API_KEY'],
    api_secret=CLOUDINARY_STORAGE['API_SECRET']
)

# جعل Cloudinary هو المخزن الافتراضي للملفات
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# المفتاح الافتراضي للأعمدة الجديدة
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# مسار تسجيل الدخول
LOGIN_URL = '/account/login/'
