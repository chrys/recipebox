from django.test import TestCase
from django.contrib.auth import get_user_model
from recipes.models import Recipe, RecipeIngredient, Category, UserScheduleMapping

User = get_user_model()

class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='catuser', password='password123')

    def test_category_user_relation(self):
        """Test that a category is associated with a user."""
        category = Category.objects.create(user=self.user, name='Personal', slug='personal')
        self.assertEqual(category.user, self.user)

class UserScheduleMappingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='scheduser', password='password123')
        self.category = Category.objects.create(user=self.user, name='Meat', slug='meat')

    def test_schedule_mapping_creation(self):
        """Test creating a schedule mapping for a specific day."""
        mapping = UserScheduleMapping.objects.create(
            user=self.user,
            day_of_week=1, # Monday
            category=self.category
        )
        self.assertEqual(mapping.get_day_of_week_display(), 'Monday')
        self.assertEqual(mapping.category, self.category)

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
