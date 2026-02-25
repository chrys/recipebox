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


from unittest.mock import patch


class RecipeParsingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

    def test_parse_recipe_text(self):
        """Test that parse_recipe_text extracts title, ingredients and steps."""
        text = """Chicken Soup

2 cups Flour
1 tsp Salt

1. Mix ingredients in a bowl.
2. Bake at 350 degrees for 20 minutes.
"""
        result = parse_recipe_text(text)

        self.assertEqual(result["title"], "Chicken Soup")
        self.assertEqual(result["ingredients"], ["2 cups Flour", "1 tsp Salt"])
        self.assertEqual(
            result["steps"],
            ["Mix ingredients in a bowl.", "Bake at 350 degrees for 20 minutes."],
        )

    def test_parse_recipe_text_no_title(self):
        """Test parsing when no title is obvious."""
        text = "2 cups Flour\n1. Cook"
        result = parse_recipe_text(text)
        self.assertEqual(result["title"], "")
        self.assertEqual(result["ingredients"], ["2 cups Flour"])
        self.assertEqual(result["steps"], ["Cook"])

    def test_parse_recipe_text_handles_varied_spacing(self):
        """Test that it handles extra whitespace and empty lines."""
        text = "  My Recipe  \n\n  Ingredient 1  \n\n  1. Step 1  "
        result = parse_recipe_text(text)
        self.assertEqual(result["title"], "My Recipe")
        self.assertEqual(result["ingredients"], ["Ingredient 1"])
        self.assertEqual(result["steps"], ["Step 1"])

    def test_recipe_from_text_prefill(self):
        """Test that posting to recipe_from_text pre-fills the creation form."""
        self.client.login(username="testuser", password="password123")
        post_data = {
            "text": "Chicken Curry\nIngredient 1\nIngredient 2\n1. Step 1\n2. Step 2"
        }
        url = reverse("recipe_from_text")
        response = self.client.post(url, post_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chicken Curry")
        self.assertContains(response, "Ingredient 1")
        self.assertContains(response, "Ingredient 2")
        self.assertContains(response, "Step 1\nStep 2")
        self.assertContains(response, "Recipe pre-filled from text!")

    def test_recipe_from_link_prefill(self):
        """Test that posting to recipe_from_link scrapes and pre-fills the form."""
        self.client.login(username="testuser", password="password123")

        with patch("recipes.views.scrape_me") as mock_scrape:
            mock_instance = mock_scrape.return_value
            mock_instance.title.return_value = "Scraped Recipe"
            mock_instance.ingredients.return_value = ["Ing 1", "Ing 2"]
            mock_instance.instructions.return_value = "Step 1\nStep 2"

            url = reverse("recipe_from_link")
            response = self.client.post(
                url, {"url": "https://example.com/recipe"}, follow=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Scraped Recipe")
            self.assertContains(response, "Ing 1")
            self.assertContains(response, "Step 1\nStep 2")
            self.assertContains(response, "Recipe scraped successfully!")

    def test_recipe_from_link_error(self):
        """Test that it handles scraping errors gracefully."""
        self.client.login(username="testuser", password="password123")

        with patch("recipes.views.scrape_me") as mock_scrape:
            mock_scrape.side_effect = Exception("Scraping failed")

            url = reverse("recipe_from_link")
            response = self.client.post(
                url, {"url": "https://example.com/recipe"}, follow=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Could not scrape the recipe from this link")
