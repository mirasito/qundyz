from django.shortcuts import render, redirect, get_object_or_404
from apps.estimates.models import Estimate, Stage
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views import View
from django.core.files.storage import default_storage
from .forms import PlanUploadForm


class EstimateIndexView(View):
    def get(self, request):
        return render(request, 'estimates/index.html')


class CalculateEstimateView(View):
    def post(self, request):
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

        # Создаём запись в БД
        estimate = Estimate.objects.create(
            user=request.user if request.user.is_authenticated else None,
            apartment_area=apartment_area,
            ceiling_height=ceiling_height,
            total_cost=Decimal(total),
            name="Предварительная смета"
        )

        return render(request, 'estimates/estimate_detail.html', {
            'estimate': estimate
        })


class PlanUploadView(View):
    def post(self, request):
        form = PlanUploadForm(request.POST, request.FILES)
        if form.is_valid():
            plan_file = form.cleaned_data['plan_file']
            path = default_storage.save('uploads/' + plan_file.name, plan_file)
            request.session['plan_file_path'] = path
            return redirect('calculate_estimate')
        return redirect('estimate_index')


def estimate_edit_view(request):
    """
    Страница редактирования предварительного расчёта сметы.
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
            return redirect('projects')
        else:
            request.session['unsaved_estimate_id'] = estimate.pk
            return redirect('user_register')
    else:
        return redirect('estimate_input')


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