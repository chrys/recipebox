from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class RecipeFormTemplateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser_ui', password='password123')
        self.client.login(username='testuser_ui', password='password123')

    def test_mandatory_asterisk_presence(self):
        response = self.client.get(reverse('recipe_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Title <span style="color: var(--color-danger, #d73a49);">*</span>')
        self.assertContains(response, 'Instructions <span style="color: var(--color-danger, #d73a49);">*</span>')
        self.assertContains(response, 'placeholder="Ingredient name *"')
