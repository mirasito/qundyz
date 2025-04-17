from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.estimates.models import Estimate  # проверьте, что импорт корректный

@login_required
def my_projects(request):
    user_estimates = Estimate.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'projects/projects.html', {'estimates': user_estimates})