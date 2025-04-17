from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Estimate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estimates', null=True, blank=True)
    name = models.CharField(max_length=255, default="Смета #1")
    apartment_area = models.FloatField()
    ceiling_height = models.FloatField()
    num_bathrooms = models.IntegerField(default=1)
    bathroom_area = models.FloatField(default=5.0)
    kitchen_area = models.FloatField(default=10.0)

    MATERIAL_QUALITY_CHOICES = [
        ('economy', 'Эконом'),
        ('standard', 'Стандарт'),
        ('premium', 'Премиум'),
    ]
    material_quality = models.CharField(
        max_length=20, choices=MATERIAL_QUALITY_CHOICES, default='standard')

    has_replanning = models.BooleanField(default=False)

    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def computed_total_cost(self):
        return sum(stage.stage_cost() for stage in self.stages.all())

    def total_duration(self):
        return sum(stage.duration_days for stage in self.stages.all())

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            from .default_data import populate_default_stages
            populate_default_stages(self)

class Stage(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name="stages")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration_days = models.IntegerField(default=1)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} (этап в смете {self.estimate.name})"

    def stage_cost(self):
        return self.total_materials_cost() + self.total_works_cost()

    def total_materials_cost(self):
        return sum(material.total_cost() for material in self.materials.all())

    def total_works_cost(self):
        return sum(work.total_cost() for work in self.works.all())

class Material(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="materials")
    name = models.CharField(max_length=200)
    quantity = models.FloatField(default=1.0)
    unit = models.CharField(max_length=50, default="шт")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"

    def total_cost(self):
        return float(self.quantity) * float(self.price_per_unit)

class Work(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="works")
    name = models.CharField(max_length=200)
    hours = models.FloatField(default=0.0)
    cost_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def total_cost(self):
        return float(self.hours) * float(self.cost_per_hour)
