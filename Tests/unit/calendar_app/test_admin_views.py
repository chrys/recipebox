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

class AdminActionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='actionuser', password='password123')
        self.client.login(username='actionuser', password='password123')

    def test_add_category(self):
        url = reverse('add_category')
        response = self.client.post(url, {'name': 'New Category'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(user=self.user, name='New Category').exists())

    def test_add_duplicate_category(self):
        Category.objects.create(user=self.user, name='Existing', slug='existing')
        url = reverse('add_category')
        response = self.client.post(url, {'name': 'Existing'})
        self.assertEqual(response.status_code, 302)
        # Verify warning message if possible, or just ensure it redirects
        self.assertEqual(Category.objects.filter(user=self.user, slug='existing').count(), 1)

    def test_delete_category(self):
        cat = Category.objects.create(user=self.user, name='Delete Me', slug='delete-me')
        url = reverse('delete_category', kwargs={'pk': cat.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Category.objects.filter(pk=cat.pk).exists())

    def test_update_schedule(self):
        cat = Category.objects.create(user=self.user, name='Meat', slug='meat')
        url = reverse('update_schedule')
        response = self.client.post(url, {
            'day': '1', # Monday
            'category': str(cat.pk)
        })
        self.assertEqual(response.status_code, 302)
        mapping = UserScheduleMapping.objects.get(user=self.user, day_of_week=1)
        self.assertEqual(mapping.category, cat)
