from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeIngredient, Category


class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Categories',
    )

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'categories',
            'prep_time', 'cook_time', 'servings',
            'instructions', 'image', 'public',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Recipe title'}),
            'description': forms.Textarea(attrs={
                'placeholder': 'A short description of the recipe…',
                'rows': 2,
            }),
            'instructions': forms.Textarea(attrs={
                'placeholder': 'One step per line…',
                'rows': 6,
            }),
            'prep_time': forms.NumberInput(attrs={'placeholder': 'mins'}),
            'cook_time': forms.NumberInput(attrs={'placeholder': 'mins'}),
            'servings': forms.NumberInput(attrs={'placeholder': 'e.g. 4'}),
        }


RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    fields=('name', 'quantity', 'order'),
    extra=3,
    can_delete=True,
    widgets={
        'name': forms.TextInput(attrs={'placeholder': 'Ingredient'}),
        'quantity': forms.TextInput(attrs={'placeholder': 'Quantity'}),
        'order': forms.HiddenInput(),
    },
)
