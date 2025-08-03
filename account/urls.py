from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    # مسار صفحة تسجيل الدخول
    path('login/', views.login_view, name='login'),

    # مسار تسجيل الخروج
    path('logout/', views.logout_view, name='logout'),
]
