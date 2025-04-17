from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_index, name='estimate_input'),
    path('calculate/', views.calculate_estimate, name='calculate_estimate'),
    path('save/<int:pk>/', views.estimate_save_view, name='estimate_save'),
    path('estimates/', views.EstimateListView.as_view(), name='estimate_list'),
    path('estimates/<int:pk>/', views.EstimateDetailView.as_view(), name='estimate_detail'),
    path('stages/<int:pk>/', views.StageDetailView.as_view(), name='stage_detail'),
]