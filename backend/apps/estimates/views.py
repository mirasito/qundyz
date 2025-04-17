from django.shortcuts import render, redirect, get_object_or_404
from apps.estimates.models import Estimate, Stage
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView

def main_index(request):
    return render(request, 'estimates/index.html')

def calculate_estimate(request):
    """
    Если форму отправляют с базовыми данными, сразу перенаправляет пользователя на страницу редактирования.
    (Можно использовать этот URL для перехода на estimate_edit_view)
    """
    if request.method == 'POST':
        try:
            apartment_area = float(request.POST.get('apartment_area', 0))
        except (TypeError, ValueError):
            apartment_area = 0.0
        try:
            ceiling_height = float(request.POST.get('ceiling_height', 0))
        except (TypeError, ValueError):
            ceiling_height = 0.0
        
        # Простая формула расчёта
        total = apartment_area * 1000 + ceiling_height * 500
        
        
         # Создаём объект в БД
        estimate = Estimate.objects.create(
            user=request.user if request.user.is_authenticated else None,
            apartment_area=apartment_area,
            ceiling_height=ceiling_height,
            total_cost=Decimal(total),
            name="Предварительная смета"
        )
        return render(request, 'estimates/estimate_detail.html', {'estimate': estimate})
    else:
        return redirect('estimate_input')


def estimate_edit_view(request):
    """
    Страница редактирования предварительного расчёта сметы.
    Доступна всем. В ней показываются базовые данные, которые можно изменить.
    """
    if request.method == 'POST':
        try:
            apartment_area = float(request.POST.get('apartment_area', 0))
        except (TypeError, ValueError):
            apartment_area = 20.0
        try:
            ceiling_height = float(request.POST.get('ceiling_height', 0))
        except (TypeError, ValueError):
            ceiling_height = 1.8

        total = apartment_area * 1000 + ceiling_height * 500

        context = {
            'estimate': {
                'name': 'Предварительная смета',
                'apartment_area': apartment_area,
                'ceiling_height': ceiling_height,
                'total_cost': total,
            }
        }
        return render(request, 'estimates/estimate_detail.html', context)
    else:
        return redirect('estimate_input')


def estimate_save_view(request, pk):
    if request.method == 'POST':
        estimate = get_object_or_404(Estimate, pk=pk)

        try:
            apartment_area = float(request.POST.get('apartment_area', 0))
        except (TypeError, ValueError):
            apartment_area = 20.0

        try:
            ceiling_height = float(request.POST.get('ceiling_height', 0))
        except (TypeError, ValueError):
            ceiling_height = 1.8

        total = apartment_area * 1000 + ceiling_height * 500

        estimate.apartment_area = apartment_area
        estimate.ceiling_height = ceiling_height
        estimate.total_cost = Decimal(total)
        estimate.name = request.POST.get('estimate_name', estimate.name)

        if request.user.is_authenticated:
            estimate.user = request.user
            estimate.save()
            return redirect('my_projects')
        else:
            request.session['unsaved_estimate_id'] = estimate.pk
            return redirect('user_register')
    else:
        return redirect('estimate_input')


# Остальные классы-представления остаются без изменений

class EstimateListView(ListView):
    model = Estimate
    template_name = 'estimates/estimate_list.html'
    context_object_name = 'estimates'

class EstimateDetailView(DetailView):
    model = Estimate
    template_name = 'estimates/estimate_detail.html'
    context_object_name = 'estimate'

class StageDetailView(DetailView):
    model = Stage
    template_name = 'estimates/stage_detail.html'
    context_object_name = 'stage'