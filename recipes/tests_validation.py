from django.test import TestCase
from django.contrib.auth import get_user_model
from recipes.models import Recipe, RecipeIngredient
from recipes.forms import RecipeForm, RecipeIngredientFormSet

User = get_user_model()

class RecipeValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_recipe_form_mandatory_fields(self):
        # Empty data
        form = RecipeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('instructions', form.errors)

    def test_ingredient_formset_partial_data_error(self):
        # Create a recipe first
        recipe = Recipe.objects.create(user=self.user, title='Test')
        
        # Partially filled ingredient: quantity but no name
        data = {
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
            'ingredients-0-name': '',
            'ingredients-0-quantity_value': '500',
            'ingredients-0-quantity_unit': 'grams',
            'ingredients-0-aisle': '',
            'ingredients-0-quantity': '',
            'ingredients-0-order': '0',
            'ingredients-0-id': '',
        }
        formset = RecipeIngredientFormSet(data, instance=recipe)
        self.assertFalse(formset.is_valid())
        # The first form should have an error on 'name'
        self.assertIn('name', formset.forms[0].errors)
        self.assertEqual(formset.forms[0].errors['name'], ['This field is required if quantity is provided.'])

    def test_ingredient_formset_empty_rows_ignored(self):
        recipe = Recipe.objects.create(user=self.user, title='Test')
        
        # Totally empty ingredient row should be valid (ignored)
        data = {
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
            'ingredients-0-name': '',
            'ingredients-0-quantity_value': '',
            'ingredients-0-quantity_unit': '',
            'ingredients-0-aisle': '',
            'ingredients-0-quantity': '',
            'ingredients-0-order': '0',
            'ingredients-0-id': '',
        }
        formset = RecipeIngredientFormSet(data, instance=recipe)
        self.assertTrue(formset.is_valid(), formset.errors)
        self.assertEqual(len(formset.save()), 0)
