from django.test import TestCase
from recipes.forms import RecipeForm, RecipeIngredientFormSet
from recipes.models import Category

class RecipeFormTest(TestCase):
    def test_required_fields(self):
        form = RecipeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('instructions', form.errors)
        # Verify specific error message if needed
        self.assertEqual(form.errors['title'], ['This field is required.'])

    def test_optional_fields(self):
        # We need to provide a title and instructions to see if it's valid with optional fields empty
        form = RecipeForm(data={
            'title': 'Test',
            'instructions': 'Test instructions'
        })
        self.assertTrue(form.is_valid())

class RecipeIngredientFormSetTest(TestCase):
    def test_ingredient_name_required(self):
        data = {
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
            'ingredients-0-quantity': '1 cup',
            'ingredients-0-name': '', # Required
            'ingredients-0-order': '0',
        }
        formset = RecipeIngredientFormSet(data=data)
        self.assertFalse(formset.is_valid())
        self.assertIn('name', formset.errors[0])

    def test_ingredient_aisle_field(self):
        data = {
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
            'ingredients-0-quantity': '1 cup',
            'ingredients-0-name': 'Milk',
            'ingredients-0-aisle': 'Dairy',
            'ingredients-0-order': '0',
        }
        formset = RecipeIngredientFormSet(data=data)
        self.assertTrue(formset.is_valid())
        self.assertEqual(formset.forms[0].cleaned_data['aisle'], 'Dairy')
