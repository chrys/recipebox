import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class RecipeRatingViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser_rating', password='password123')
        self.recipe = Recipe.objects.create(
            user=self.user,
            title='Rating Test Recipe',
            instructions='Step 1'
        )
        self.url = reverse('recipe_update_rating', kwargs={'pk': self.recipe.pk})

    def test_update_rating_authenticated(self):
        """Test that an authenticated user can update a recipe rating."""
        self.client.login(username='testuser_rating', password='password123')
        response = self.client.post(
            self.url,
            data=json.dumps({'rating': 4}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['rating'], 4)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.rating, 4)

    def test_update_rating_unauthenticated(self):
        """Test that an unauthenticated user cannot update a recipe rating."""
        response = self.client.post(
            self.url,
            data=json.dumps({'rating': 4}),
            content_type='application/json'
        )
        # Should redirect to login or return 403. Let's assume 403 for API-like calls or redirect.
        # Since it's AJAX, we might return 403.
        self.assertEqual(response.status_code, 302) # Redirect to login

    def test_update_rating_invalid_json(self):
        """Test that invalid JSON data is rejected."""
        self.client.login(username='testuser_rating', password='password123')
        response = self.client.post(
            self.url,
            data='invalid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid data')

    def test_update_rating_invalid_value(self):
        """Test that invalid rating values are rejected."""
        self.client.login(username='testuser_rating', password='password123')
        response = self.client.post(
            self.url,
            data=json.dumps({'rating': 6}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid rating')
