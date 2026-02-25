from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.urls import reverse
from recipes.models import Ingredient, Recipe, RecipeIngredient

User = get_user_model()


class IngredientModelTest(TestCase):
    def test_ingredient_model_exists(self):
        """Test that the Ingredient model is defined."""
        self.assertIsNotNone(
            Ingredient, "Ingredient model should be defined in recipes.models"
        )

    def test_ingredient_fields(self):
        """Test the fields of the Ingredient model."""
        user = User.objects.create_user(username="testuser", password="password123")
        ingredient = Ingredient.objects.create(name="Onion", user=user)

        self.assertEqual(ingredient.name, "Onion")
        self.assertEqual(ingredient.user, user)
        self.assertTrue(hasattr(ingredient, "created_at"))

    def test_ingredient_unique_per_user(self):
        """Test that ingredient names are unique per user (or global)."""
        user = User.objects.create_user(username="testuser2", password="password123")
        Ingredient.objects.create(name="Garlic", user=user)

        with self.assertRaises(IntegrityError):
            Ingredient.objects.create(name="Garlic", user=user)

    def test_ingredient_global_option(self):
        """Test that an ingredient can be global (user=null)."""
        ingredient = Ingredient.objects.create(name="Salt", user=None)
        self.assertIsNone(ingredient.user)


class AutoPersistTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="persistuser", password="password123"
        )
        self.recipe = Recipe.objects.create(
            user=self.user, title="Test Recipe", instructions="Step 1"
        )

    def test_recipe_ingredient_save_persists_to_master(self):
        """Test that saving a RecipeIngredient adds the name to the Ingredient table."""
        RecipeIngredient.objects.create(
            recipe=self.recipe, name="Fresh Basil", quantity="1 bunch"
        )

        # Check if it exists in Ingredient table
        exists = Ingredient.objects.filter(user=self.user, name="Fresh Basil").exists()
        self.assertTrue(
            exists,
            "Ingredient 'Fresh Basil' should have been persisted to master table",
        )

    def test_recipe_ingredient_save_no_duplicates(self):
        """Test that saving same ingredient twice doesn't crash (upsert)."""
        # First save
        RecipeIngredient.objects.create(
            recipe=self.recipe, name="Garlic", quantity="2 cloves"
        )
        # Second save (same name)
        RecipeIngredient.objects.create(
            recipe=self.recipe, name="Garlic", quantity="1 clove"
        )

        count = Ingredient.objects.filter(user=self.user, name="Garlic").count()
        self.assertEqual(
            count, 1, "Should only have one entry in master table for 'Garlic'"
        )

    def test_recipe_ingredient_save_strips_whitespace(self):
        """Test that whitespace is stripped before persisting."""
        RecipeIngredient.objects.create(
            recipe=self.recipe, name="  Cumin  ", quantity="1 tsp"
        )

        exists = Ingredient.objects.filter(user=self.user, name="Cumin").exists()
        self.assertTrue(exists, "Ingredient should be persisted without whitespace")


class AutocompleteAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="password123")
        # Add some historical ingredients
        Ingredient.objects.create(user=self.user, name="Onion")
        Ingredient.objects.create(user=self.user, name="Garlic")
        # Add some from another user (should NOT show up unless global)
        other_user = User.objects.create_user(
            username="otheruser", password="password123"
        )
        Ingredient.objects.create(user=other_user, name="Ginger")
        # Add a global one
        Ingredient.objects.create(user=None, name="Salt")

    def test_autocomplete_endpoint_returns_json(self):
        """Test that the autocomplete endpoint returns a JSON response."""
        self.client.login(username="apiuser", password="password123")
        response = self.client.get("/recipes/ingredients/autocomplete/?q=oni")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = response.json()
        self.assertIn("suggestions", data)

    def test_autocomplete_filters_by_query(self):
        """Test that the autocomplete filters suggestions by query."""
        self.client.login(username="apiuser", password="password123")
        response = self.client.get("/recipes/ingredients/autocomplete/?q=oni")
        data = response.json()
        suggestions = data["suggestions"]
        self.assertIn("Onion", suggestions)
        self.assertNotIn("Garlic", suggestions)

    def test_autocomplete_includes_global_ingredients(self):
        """Test that global ingredients are included in suggestions."""
        self.client.login(username="apiuser", password="password123")
        response = self.client.get("/recipes/ingredients/autocomplete/?q=sal")
        data = response.json()
        self.assertIn("Salt", data["suggestions"])

    def test_autocomplete_excludes_other_users_ingredients(self):
        """Test that other users' ingredients are not suggested."""
        self.client.login(username="apiuser", password="password123")
        response = self.client.get("/recipes/ingredients/autocomplete/?q=gin")
        data = response.json()
        self.assertNotIn("Ginger", data["suggestions"])


class AutocompleteUITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="uiuser", password="password123")

    def test_ingredient_name_field_has_autocomplete_url(self):
        """Test that the ingredient name input has the correct data-autocomplete-url."""
        self.client.login(username="uiuser", password="password123")
        response = self.client.get(reverse("recipe_create"))
        self.assertEqual(response.status_code, 200)

        # Check for data-autocomplete-url in the HTML
        expected_url = reverse("ingredient_autocomplete")
        self.assertContains(response, f'data-autocomplete-url="{expected_url}"')
