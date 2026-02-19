from django.test import TestCase
from recipes.models import Recipe, RecipeIngredient, Category
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class RecipeIngredientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.recipe = Recipe.objects.create(user=self.user, title='Test Recipe')

    def test_recipe_ingredient_new_quantity_fields(self):
        # This test should fail because these fields don't exist yet
        ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            name='Flour',
            quantity_value=500,
            quantity_unit='grams'
        )
        
        self.assertEqual(ingredient.quantity_value, 500)
        self.assertEqual(ingredient.quantity_unit, 'grams')
        self.assertEqual(str(ingredient), '500 grams Flour')

    def test_recipe_ingredient_unit_choices(self):
        # Verify that we can only use allowed units
        # This will also fail initially
        valid_units = ['grams', 'kilograms', 'cups', 'tsp', 'tbsp', 'piece']
        for unit in valid_units:
            ingredient = RecipeIngredient.objects.create(
                recipe=self.recipe,
                name='Test',
                quantity_value=1,
                quantity_unit=unit
            )
            self.assertEqual(ingredient.quantity_unit, unit)
