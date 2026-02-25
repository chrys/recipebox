from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

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
