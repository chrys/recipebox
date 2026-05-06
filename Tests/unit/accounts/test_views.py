from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from unittest.mock import patch
import json

User = get_user_model()


class CustomLoginViewTest(TestCase):
    def setUp(self):
        self.url = reverse('account_login')

    def test_get_renders_login_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="email"', response.content)  # Form field should be in HTML
        self.assertIn(b'id="password"', response.content)


class CustomLogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='logoutuser', password='TestPass99!'
        )
        self.url = reverse('account_logout')

    def test_logout_redirects_to_login(self):
        self.client.login(username='logoutuser', password='TestPass99!')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('account_login'), response.url)

    def test_user_is_actually_logged_out(self):
        self.client.login(username='logoutuser', password='TestPass99!')
        self.client.post(self.url)
        self.assertNotIn('_auth_user_id', self.client.session)


class SignupViewTest(TestCase):
    def setUp(self):
        self.url = reverse('account_signup')

    def test_get_renders_signup_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'id="email"', response.content)
        self.assertIn(b'id="password"', response.content)


class FirebaseLoginTest(TestCase):
    def setUp(self):
        self.url = reverse('firebase_login')
        
    @patch('accounts.views.firebase_admin.auth.verify_id_token')
    def test_valid_firebase_login_creates_user_and_logs_in(self, mock_verify):
        mock_verify.return_value = {'email': 'brand@new.com', 'uid': '12345'}
        
        response = self.client.post(self.url, json.dumps({'id_token': 'fake_token'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # User should exist
        self.assertTrue(User.objects.filter(email='brand@new.com').exists())
        # Should be auto-logged-in
        self.assertIn('_auth_user_id', self.client.session)

    def test_missing_token_returns_error(self):
        response = self.client.post(self.url, json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    @patch('accounts.views.firebase_admin.auth.verify_id_token')
    def test_firebase_login_autosaves_guest_recipe_draft(self, mock_verify):
        mock_verify.return_value = {'email': 'draft@new.com', 'uid': '12345'}
        
        session = self.client.session
        session['guest_recipe_draft'] = {
            'recipe': {
                'title': 'Session Draft',
                'description': 'Draft description',
                'instructions': 'Step one',
                'prep_time': 10,
                'cook_time': 20,
                'servings': 2,
                'public': True,
            },
            'ingredients': [
                {
                    'name': 'Onion',
                    'quantity_value': '1',
                    'quantity_unit': 'piece',
                    'quantity': '',
                    'aisle': 'Produce',
                    'order': 0,
                }
            ],
        }
        session.save()

        response = self.client.post(self.url, json.dumps({'id_token': 'fake_token'}), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email='draft@new.com').exists())

        recipe = Recipe.objects.get(title='Session Draft')
        self.assertEqual(recipe.user.email, 'draft@new.com')
        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertNotIn('guest_recipe_draft', self.client.session)
