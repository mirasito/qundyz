from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from apps.estimates.models import Estimate

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Сохраняем предварительную смету в сессии
            # чтобы потом использовать её при регистрации
            unsaved = request.session.get('unsaved_estimate')
            if unsaved:
                from decimal import Decimal
                Estimate.objects.create(
                    user=user,
                    apartment_area=unsaved.get('apartment_area', 0),
                    ceiling_height=unsaved.get('ceiling_height', 0),
                    total_cost=Decimal(unsaved.get('total_cost', 0))
                )
                del request.session['unsaved_estimate']
            return redirect('user_profile')
            return redirect('user_profile')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')