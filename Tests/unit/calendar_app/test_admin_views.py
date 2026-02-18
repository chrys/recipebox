from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Category, UserScheduleMapping

User = get_user_model()

class AdminSettingsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='adminuser', password='password123')
        self.url = reverse('admin_settings')

    def test_view_accessible_authenticated(self):
        self.client.login(username='adminuser', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/admin_settings.html')

    def test_view_redirect_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_view_context(self):
        self.client.login(username='adminuser', password='password123')
        cat = Category.objects.create(user=self.user, name='Test Cat', slug='test-cat')
        mapping = UserScheduleMapping.objects.create(user=self.user, day_of_week=1, category=cat)
        
        response = self.client.get(self.url)
        self.assertIn('categories', response.context)
        self.assertIn('mappings', response.context)
        self.assertIn('days', response.context)
