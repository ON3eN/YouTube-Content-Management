from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def tasks_view(request):
    return render(request, 'reviewer/tasks.html')


@login_required
def review_view(request):
    return render(request, 'reviewer/review.html')  # للتأكيد أو الرفض
