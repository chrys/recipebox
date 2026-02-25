from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe, RecipeIngredient

User = get_user_model()


class IngredientDisplayTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="TestPass99!"
        )
        self.recipe = Recipe.objects.create(
            user=self.user, title="Test Recipe", instructions="Test instructions"
        )
        # Create an ingredient with decimal quantity
        RecipeIngredient.objects.create(
            recipe=self.recipe,
            name="Ingredient 1",
            quantity_value="2.00",
            quantity_unit="cups",
        )
        # Create an ingredient with fractional decimal quantity
        RecipeIngredient.objects.create(
            recipe=self.recipe,
            name="Ingredient 2",
            quantity_value="0.50",
            quantity_unit="kg",
        )
        # Create an empty ingredient
        RecipeIngredient.objects.create(
            recipe=self.recipe, name="", quantity_value=None, quantity_unit=""
        )

    def test_no_empty_bullet_points(self):
        """
        Verify that ingredients with empty names are not rendered as bullet points.
        """
        self.client.login(username="testuser", password="TestPass99!")
        url = reverse("recipe_detail", kwargs={"pk": self.recipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check that we don't have an empty <li> for the blank ingredient
        # The exact HTML depends on the template, but we expect no <li></li> or <li>\s*</li>
        # based on empty name.
        content = response.content.decode()
        # If the template renders <li>{{ ingredient.quantity }} {{ ingredient.unit }} {{ ingredient.name }}</li>
        # for an empty ingredient it might look like <li>   </li>
        import re

        # Look for <li> tags that don't have non-whitespace text after the opening tag
        # excluding the <strong> tags if they are empty
        empty_li_pattern = re.compile(r"<li[^>]*>\s*(?:<strong>\s*</strong>)?\s*</li>")
        self.assertFalse(
            empty_li_pattern.search(content),
            "Found empty <li> element in ingredient list",
        )

    def test_quantity_normalization(self):
        """
        Verify that trailing zeros are stripped from quantity display.
        """
        self.client.login(username="testuser", password="TestPass99!")
        url = reverse("recipe_detail", kwargs={"pk": self.recipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()
        self.assertIn("2 cups", content)
        self.assertNotIn("2.00 cups", content)
        self.assertIn("0.5 kg", content)
        self.assertNotIn("0.50 kg", content)
