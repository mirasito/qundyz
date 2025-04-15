from django.contrib import admin
from .models import Estimate, Stage, Material, Work

@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "total_cost")

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ("name", "estimate", "duration_days", "stage_cost")

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "stage", "quantity", "unit", "price_per_unit", "total_cost")

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("name", "stage", "hours", "cost_per_hour", "total_cost")