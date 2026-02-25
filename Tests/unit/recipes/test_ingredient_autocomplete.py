from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from recipes.models import Ingredient

User = get_user_model()


class IngredientModelTest(TestCase):
    def test_ingredient_model_exists(self):
        """Test that the Ingredient model is defined."""
        self.assertIsNotNone(
            Ingredient, "Ingredient model should be defined in recipes.models"
        )

    def test_ingredient_fields(self):
        """Test the fields of the Ingredient model."""
        if Ingredient is None:
            self.fail("Ingredient model not found")

        user = User.objects.create_user(username="testuser", password="password123")
        ingredient = Ingredient.objects.create(name="Onion", user=user)

        self.assertEqual(ingredient.name, "Onion")
        self.assertEqual(ingredient.user, user)
        self.assertTrue(hasattr(ingredient, "created_at"))

    def test_ingredient_unique_per_user(self):
        """Test that ingredient names are unique per user (or global)."""
        if Ingredient is None:
            self.fail("Ingredient model not found")

        user = User.objects.create_user(username="testuser2", password="password123")
        Ingredient.objects.create(name="Garlic", user=user)

        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(name="Garlic", user=user)

    def test_ingredient_global_option(self):
        """Test that an ingredient can be global (user=null)."""
        if Ingredient is None:
            self.fail("Ingredient model not found")

        ingredient = Ingredient.objects.create(name="Salt", user=None)
        self.assertIsNone(ingredient.user)
