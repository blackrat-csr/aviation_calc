from django.db import models
import math

# Create your models here.

class CalculationHistory(models.Model):
    CALCULATION_TYPES = [
        ('wind_triangle', 'Wind Triangle'),
        ('great_circle', 'Great Circle'),
        ('rhumb_line', 'Rhumb Line'),
    ]
    
    calculation_type = models.CharField(max_length=20, choices=CALCULATION_TYPES)
    inputs = models.JSONField()
    results = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_calculation_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
