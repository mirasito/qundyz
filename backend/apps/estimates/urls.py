from django.urls import path
from .views import (
    EstimateIndexView,
    CalculateEstimateView,
    PlanUploadView,
    estimate_save_view,
    EstimateListView,
    EstimateDetailView,
    StageDetailView
)

urlpatterns = [
    path('', EstimateIndexView.as_view(), name='estimate_index'),
    path('calculate/', CalculateEstimateView.as_view(), name='calculate_estimate'),
    path('upload_plan/', PlanUploadView.as_view(), name='upload_plan'),
    path('save/<int:pk>/', estimate_save_view, name='estimate_save'),
    path('estimates/', EstimateListView.as_view(), name='estimate_list'),
    path('estimates/<int:pk>/', EstimateDetailView.as_view(), name='estimate_detail'),
    path('stages/<int:pk>/', StageDetailView.as_view(), name='stage_detail'),
]