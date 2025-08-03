from django.urls import path
from .views import home_view

app_name = 'workflow'

urlpatterns = [
    path('', home_view, name='home'),  # ← صار المسار الأساسي للتطبيق
]
