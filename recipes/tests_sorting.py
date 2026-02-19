from django.test import TestCase
from django.contrib.auth import get_user_model
from recipes.models import Category
from django.urls import reverse

User = get_user_model()

class CategorySortingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create categories in non-alphabetical order
        Category.objects.create(name='Zucchini', slug='zucchini', user=self.user)
        Category.objects.create(name='Apple', slug='apple', user=self.user)
        Category.objects.create(name='Banana', slug='banana', user=self.user)

    def test_category_ordering_alphabetical(self):
        categories = list(Category.objects.filter(user=self.user).values_list('name', flat=True))
        self.assertEqual(categories, ['Apple', 'Banana', 'Zucchini'])

    def test_category_sorting_in_sidebar(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('recipe_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check that categories in context are sorted (filter for our user's categories)
        categories_in_ctx = list(response.context['categories'].filter(user=self.user).values_list('name', flat=True))
        self.assertEqual(categories_in_ctx, ['Apple', 'Banana', 'Zucchini'])

    def test_category_sorting_in_admin_settings(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('admin_settings'))
        self.assertEqual(response.status_code, 200)
        
        if 'categories' in response.context:
            categories_in_ctx = list(response.context['categories'].filter(user=self.user).values_list('name', flat=True))
            self.assertEqual(categories_in_ctx, ['Apple', 'Banana', 'Zucchini'])
