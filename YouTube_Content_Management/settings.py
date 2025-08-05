"""
إعدادات مشروع YouTube_Content_Management باستخدام Django 5.2.4

توثيق الإعدادات:
https://docs.djangoproject.com/en/5.2/topics/settings/
"""

from pathlib import Path

# المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# مفتاح الأمان (يجب تغييره في الإنتاج)
SECRET_KEY = 'django-insecure-5+=6#o*dtt^@zha^iyo58f=9tq6_d&!f82i=7syv^guqz2@tox'

# تفعيل وضع التطوير
DEBUG = True

# قائمة العناوين المسموح بها (أضفドومينك في الإنتاج)
ALLOWED_HOSTS = []

# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # التطبيقات المخصصة
    'account',
    'workflow',
    'youtuber',
    'editor',
    'thumbnailer',
    'reviewer',
    'publisher',
]

# الوسطاء
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # لدعم اللغات
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
        'DIRS': [BASE_DIR / 'templates'],  # مجلد القوالب
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

# تطبيق WSGI
WSGI_APPLICATION = 'YouTube_Content_Management.wsgi.application'

# قاعدة البيانات (SQLite مؤقتًا)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# تحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# اللغة والتوقيت
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# الملفات الثابتة (Static)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # لتجميع static ب collectstatic

# ملفات الوسائط (Media)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# نوع المفتاح الافتراضي
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
