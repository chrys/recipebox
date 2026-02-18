from django import forms
from .models import CalendarEntry
from recipes.models import Recipe


class CalendarEntryForm(forms.ModelForm):
    class Meta:
        model = CalendarEntry
        fields = ['recipe', 'date', 'meal_type']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['recipe'].queryset = Recipe.objects.filter(user=user)
