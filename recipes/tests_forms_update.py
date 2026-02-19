from django.test import TestCase
from django.contrib.auth import get_user_model
from recipes.models import Recipe, RecipeIngredient
from recipes.forms import RecipeIngredientFormSet

User = get_user_model()

class RecipeFormUpdateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.recipe = Recipe.objects.create(user=self.user, title='Test Recipe')

    def test_ingredient_formset_has_new_fields(self):
        formset = RecipeIngredientFormSet(instance=self.recipe)
        # Check if new fields are in the form widgets
        for form in formset:
            self.assertIn('quantity_value', form.fields)
            self.assertIn('quantity_unit', form.fields)
            
    def test_ingredient_formset_save(self):
        data = {
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
            'ingredients-0-name': 'Flour',
            'ingredients-0-quantity_value': '500',
            'ingredients-0-quantity_unit': 'grams',
            'ingredients-0-aisle': 'Baking',
            'ingredients-0-order': '0',
            'ingredients-0-id': '',
        }
        formset = RecipeIngredientFormSet(data, instance=self.recipe)
        self.assertTrue(formset.is_valid(), formset.errors)
        formset.save()
        
        self.assertEqual(self.recipe.ingredients.count(), 1)
        ingredient = self.recipe.ingredients.first()
        self.assertEqual(ingredient.name, 'Flour')
        self.assertEqual(ingredient.quantity_value, 500)
        self.assertEqual(ingredient.quantity_unit, 'grams')
