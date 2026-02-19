from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomLoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='loginuser', password='TestPass99!'
        )
        self.url = reverse('account_login')

    def test_get_renders_login_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username', response.content)  # Form field should be in HTML

    def test_valid_login_redirects(self):
        response = self.client.post(self.url, {
            'username': 'loginuser',
            'password': 'TestPass99!',
        })
        # Should redirect to LOGIN_REDIRECT_URL
        self.assertEqual(response.status_code, 302)

    def test_invalid_credentials_shows_form(self):
        response = self.client.post(self.url, {
            'username': 'loginuser',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username', response.content)  # Form should be re-rendered
        # Form should contain errors (check for error messages in HTML)
        self.assertIn(b'login failed', response.content.lower())

    def test_authenticated_user_redirected(self):
        """An already-authenticated user visiting the login page is redirected."""
        self.client.login(username='loginuser', password='TestPass99!')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


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
        # Accessing a login-required page should redirect
        response = self.client.get(reverse('recipe_list'))
        self.assertEqual(response.status_code, 302)


class SignupViewTest(TestCase):
    def setUp(self):
        self.url = reverse('account_signup')

    def test_get_renders_signup_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username', response.content)  # Form field should be in HTML

    def test_valid_signup_creates_user_and_logs_in(self):
        response = self.client.post(self.url, {
            'username': 'brand_new',
            'email': 'brand@new.com',
            'password1': 'StrongPass99!',
            'password2': 'StrongPass99!',
        })
        self.assertEqual(response.status_code, 302)
        # User should exist
        self.assertTrue(User.objects.filter(username='brand_new').exists())
        # Should be auto-logged-in; accessing login-required page should work
        resp = self.client.get(reverse('recipe_list'))
        self.assertEqual(resp.status_code, 200)

    def test_invalid_signup_rerenders_form(self):
        response = self.client.post(self.url, {
            'username': '',
            'email': '',
            'password1': 'x',
            'password2': 'y',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username', response.content)  # Form should be re-rendered
        # No user created
        self.assertEqual(User.objects.count(), 0)

    def test_signup_redirects_to_recipe_list(self):
        response = self.client.post(self.url, {
            'username': 'redir_user',
            'email': 'r@d.com',
            'password1': 'StrongPass99!',
            'password2': 'StrongPass99!',
        })
        self.assertRedirects(response, reverse('recipe_list'))
