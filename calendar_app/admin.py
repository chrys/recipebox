from django.contrib import admin
from .models import CalendarEntry


@admin.register(CalendarEntry)
class CalendarEntryAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'date', 'meal_type')
    list_filter = ('meal_type', 'date')
    search_fields = ('recipe__title',)
