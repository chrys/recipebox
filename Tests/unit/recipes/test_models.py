from django.test import TestCase
from django.contrib.auth import get_user_model
from recipes.models import Recipe, RecipeIngredient

User = get_user_model()

class RecipeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='Test Recipe',
            instructions='Step 1'
        )

    def test_recipe_has_rating_field(self):
        """Test that the recipe model has a rating field."""
        self.recipe.rating = 5
        self.recipe.save()
        refreshed_recipe = Recipe.objects.get(pk=self.recipe.pk)
        self.assertEqual(refreshed_recipe.rating, 5)

class RecipeIngredientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser_ing', password='password123')
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='Test Recipe for Ingredient',
            instructions='Step 1'
        )
        self.ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            name='Salt',
            quantity='1 tsp'
        )

    def test_ingredient_has_aisle_field(self):
        """Test that the ingredient model has an aisle field."""
        self.ingredient.aisle = 'Spices'
        self.ingredient.save()
        refreshed_ingredient = RecipeIngredient.objects.get(pk=self.ingredient.pk)
        self.assertEqual(refreshed_ingredient.aisle, 'Spices')
