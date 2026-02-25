from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()


class RecipeListSortingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="sortuser", password="password123"
        )
        # Create recipes out of order
        Recipe.objects.create(user=self.user, title="Banana Bread", instructions="...")
        Recipe.objects.create(user=self.user, title="Apple Pie", instructions="...")
        Recipe.objects.create(user=self.user, title="Cherry Tart", instructions="...")
        self.url = reverse("recipe_list")

    def test_recipes_sorted_alphabetically(self):
        """Test that recipes are returned in A-Z order by title."""
        self.client.login(username="sortuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        recipes = response.context["recipes"]
        titles = [r.title for r in recipes]

        expected_titles = sorted(["Banana Bread", "Apple Pie", "Cherry Tart"])
        self.assertEqual(
            titles, expected_titles, f"Recipes should be sorted A-Z. Got {titles}"
        )
