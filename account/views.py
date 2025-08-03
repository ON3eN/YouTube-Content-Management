from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from account.models import الملف_الشخصي
from django.contrib.auth.decorators import login_required

def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('home')

    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # المحاولة باسم المستخدم
        user = authenticate(request, username=username_or_email, password=password)

        # المحاولة بالبريد الإلكتروني إذا فشلت السابقة
        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)

            # تأكد من وجود الملف الشخصي أو أنشئه إن لم يوجد
            الملف_الشخصي.objects.get_or_create(المستخدم=user)

            return redirect(next_url)

    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('account:login')
