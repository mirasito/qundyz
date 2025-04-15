from django.views.generic import ListView, DetailView
from .models import Estimate, Stage
from django.shortcuts import render, redirect

def main_index(request):
    # Здесь рендерим ваш файл: 'index.html' 
    return render(request, 'estimates/index.html')

def calculate_estimate(request):
    if request.method == 'POST':
        # Здесь вы можете получить данные формы из request.POST
        # Для примера мы используем статически подготовленные данные.
        sample_estimate = {
            'name': 'Смета #1',
            'total_cost': 123456.78,
            'stages': [
                {
                    'name': 'Подготовка поверхности',
                    'cost': 10000,
                    'works': [
                        {'name': 'Очистка стен', 'hours': 5, 'cost_per_hour': 100, 'total_cost': 500},
                        {'name': 'Уборка', 'hours': 2, 'cost_per_hour': 50, 'total_cost': 100},
                    ],
                    'materials': [
                        {'name': 'Шпаклевка', 'quantity': 10, 'unit': 'кг', 'price_per_unit': 30, 'total_cost': 300},
                    ]
                },
                {
                    'name': 'Отделка стен',
                    'cost': 20000,
                    'works': [
                        {'name': 'Покраска', 'hours': 8, 'cost_per_hour': 120, 'total_cost': 960},
                    ],
                    'materials': [
                        {'name': 'Краска', 'quantity': 5, 'unit': 'литр', 'price_per_unit': 200, 'total_cost': 1000},
                    ]
                }
            ]
        }
        # Перейдем в шаблон с результатом расчёта
        return render(request, 'estimates/estimate_detail.html', {'estimate': sample_estimate})
    else:
        return redirect('main_index')
    
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