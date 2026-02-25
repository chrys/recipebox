from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.utils import parse_recipe_text

User = get_user_model()


class RecipeCreateModesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.url = reverse("recipe_create")

    def test_tabs_present_on_create(self):
        """Test that Form, Create from text, and Create from link tabs are present."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertContains(response, "Form")
        self.assertContains(response, "Create from text")
        self.assertContains(response, "Create from link")


class RecipeParsingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

    def test_parse_recipe_text(self):
        """Test that parse_recipe_text extracts ingredients and steps."""
        text = """
2 cups Flour
1 tsp Salt

1. Mix ingredients in a bowl.
2. Bake at 350 degrees for 20 minutes.
"""
        result = parse_recipe_text(text)

        expected_ingredients = ["2 cups Flour", "1 tsp Salt"]
        expected_steps = [
            "Mix ingredients in a bowl.",
            "Bake at 350 degrees for 20 minutes.",
        ]

        self.assertEqual(result["ingredients"], expected_ingredients)
        self.assertEqual(result["steps"], expected_steps)

    def test_parse_recipe_text_handles_varied_spacing(self):
        """Test that it handles extra whitespace and empty lines."""
        text = "  Ingredient 1  \n\n  1. Step 1  "
        result = parse_recipe_text(text)
        self.assertEqual(result["ingredients"], ["Ingredient 1"])
        self.assertEqual(result["steps"], ["Step 1"])

    def test_recipe_from_text_prefill(self):
        """Test that posting to recipe_from_text pre-fills the creation form."""
        self.client.login(username="testuser", password="password123")
        post_data = {"text": "Ingredient 1\nIngredient 2\n1. Step 1\n2. Step 2"}
        url = reverse("recipe_from_text")
        response = self.client.post(url, post_data, follow=True)

        self.assertEqual(response.status_code, 200)
        # Check if pre-filled data is in the form
        self.assertContains(response, "Ingredient 1")
        self.assertContains(response, "Ingredient 2")
        # Instructions should have steps separated by newlines
        self.assertContains(response, "Step 1\nStep 2")
