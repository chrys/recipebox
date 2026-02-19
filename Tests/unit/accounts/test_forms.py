from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.forms import SignupForm

User = get_user_model()


class SignupFormValidDataTest(TestCase):
    def test_valid_signup_creates_user(self):
        """A form with valid data should be valid and save a new user."""
        form = SignupForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass99!',
            'password2': 'StrongPass99!',
        })
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'new@example.com')

    def test_email_is_optional(self):
        """Email is not required on Django's default User model."""
        form = SignupForm(data={
            'username': 'noemail',
            'email': '',
            'password1': 'StrongPass99!',
            'password2': 'StrongPass99!',
        })
        self.assertTrue(form.is_valid(), form.errors)


class SignupFormMissingFieldsTest(TestCase):
    def test_missing_username(self):
        form = SignupForm(data={
            'username': '',
            'email': 'a@b.com',
            'password1': 'StrongPass99!',
            'password2': 'StrongPass99!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_missing_password1(self):
        form = SignupForm(data={
            'username': 'user1',
            'email': 'a@b.com',
            'password1': '',
            'password2': 'StrongPass99!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_missing_password2(self):
        form = SignupForm(data={
            'username': 'user1',
            'email': 'a@b.com',
            'password1': 'StrongPass99!',
            'password2': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_completely_empty_form(self):
        form = SignupForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)


class SignupFormPasswordMismatchTest(TestCase):
    def test_password_mismatch(self):
        form = SignupForm(data={
            'username': 'mismatch',
            'email': 'a@b.com',
            'password1': 'StrongPass99!',
            'password2': 'DifferentPass88!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class SignupFormDuplicateUsernameTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='existing', password='Password99!')

    def test_duplicate_username_rejected(self):
        form = SignupForm(data={
            'username': 'existing',
            'email': 'dup@b.com',
            'password1': 'StrongPass99!',
            'password2': 'StrongPass99!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class SignupFormWeakPasswordTest(TestCase):
    def test_too_short_password(self):
        form = SignupForm(data={
            'username': 'shortpw',
            'email': 'a@b.com',
            'password1': 'Ab1!',
            'password2': 'Ab1!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_common_password(self):
        form = SignupForm(data={
            'username': 'commonpw',
            'email': 'a@b.com',
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertFalse(form.is_valid())

    def test_numeric_only_password(self):
        form = SignupForm(data={
            'username': 'numpw',
            'email': 'a@b.com',
            'password1': '83927461058',
            'password2': '83927461058',
        })
        self.assertFalse(form.is_valid())
