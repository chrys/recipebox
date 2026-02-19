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


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ('name', 'quantity_value', 'quantity_unit', 'quantity', 'aisle', 'order')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingredient name *'}),
            'quantity_value': forms.NumberInput(attrs={'placeholder': 'Val', 'step': '0.01'}),
            'quantity_unit': forms.Select(),
            'quantity': forms.TextInput(attrs={'placeholder': 'Notes (e.g. "a pinch")'}),
            'aisle': forms.TextInput(attrs={'placeholder': 'Aisle'}),
            'order': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make name optional in the form so the formset can ignore empty rows
        self.fields['name'].required = False

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        # If any of these are filled, then name MUST be provided
        val = cleaned_data.get('quantity_value')
        unit = cleaned_data.get('quantity_unit')
        
        if (val or unit) and not name:
            self.add_error('name', 'This field is required if quantity is provided.')
        return cleaned_data

RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=3,
    can_delete=True,
)
