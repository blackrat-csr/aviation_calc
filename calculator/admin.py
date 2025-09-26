from django.contrib import admin
from .models import CalculationHistory

@admin.register(CalculationHistory)
class CalculationHistoryAdmin(admin.ModelAdmin):
    list_display = ('calculation_type', 'created_at')
    list_filter = ('calculation_type', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
