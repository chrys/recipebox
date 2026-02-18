from django.conf import settings
from django.db import models


class CalendarEntry(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='calendar_entries',
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='calendar_entries',
    )
    date = models.DateField()
    meal_type = models.CharField(
        max_length=20,
        choices=MEAL_TYPE_CHOICES,
        default='dinner',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'meal_type']
        unique_together = ['user', 'recipe', 'date', 'meal_type']
        verbose_name_plural = 'Calendar entries'

    def __str__(self):
        return f'{self.recipe.title} — {self.date} ({self.get_meal_type_display()})'
