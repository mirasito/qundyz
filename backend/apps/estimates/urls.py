from django.urls import path
from . import views

urlpatterns = [
    path('estimates/', views.EstimateListView.as_view(), name='estimate_list'),
    path('estimates/<int:pk>/', views.EstimateDetailView.as_view(), name='estimate_detail'),
    path('stages/<int:pk>/', views.StageDetailView.as_view(), name='stage_detail'),
    path('', views.main_index, name='main_index'),
    path('calculate/', views.calculate_estimate, name='calculate_estimate'),
]