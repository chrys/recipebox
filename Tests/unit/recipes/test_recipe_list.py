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
        # Create recipes out of order and with mixed casing
        Recipe.objects.create(user=self.user, title="Banana Bread", instructions="...")
        Recipe.objects.create(user=self.user, title="apple pie", instructions="...")
        Recipe.objects.create(user=self.user, title="Cherry Tart", instructions="...")
        self.url = reverse("recipe_list")

    def test_recipes_sorted_alphabetically(self):
        """Test that recipes are returned in A-Z order by title (case-insensitive)."""
        self.client.login(username="sortuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        recipes = response.context["recipes"]
        titles = [r.title for r in recipes]

        expected_titles = ["apple pie", "Banana Bread", "Cherry Tart"]
        self.assertEqual(
            titles,
            expected_titles,
            f"Recipes should be sorted A-Z (case-insensitive). Got {titles}",
        )


class RecipeListViewToggleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="toggleuser", password="password123"
        )
        self.url = reverse("recipe_list")

    def test_toggle_button_present(self):
        """Test that the grid/list toggle button is present in the template."""
        self.client.login(username="toggleuser", password="password123")
        response = self.client.get(self.url)
        self.assertContains(response, 'id="view-toggle"')

    def test_list_view_container_present(self):
        """Test that the list-view container is present in the template."""
        Recipe.objects.create(user=self.user, title="Test Recipe", instructions="...")
        self.client.login(username="toggleuser", password="password123")
        response = self.client.get(self.url)
        self.assertContains(response, 'id="recipe-list-view"')
        self.assertContains(response, 'id="recipe-grid-view"')
