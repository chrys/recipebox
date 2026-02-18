from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Category
from calendar_app.models import CalendarEntry
from datetime import date

User = get_user_model()

class ReplaceRecipeLogicTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='replaceuser', password='password123')
        self.client.login(username='replaceuser', password='password123')
        
        self.cat = Category.objects.create(user=self.user, name='Fish', slug='fish')
        self.recipe1 = Recipe.objects.create(user=self.user, title='Salmon', instructions='Bake')
        self.recipe1.categories.add(self.cat)
        self.recipe2 = Recipe.objects.create(user=self.user, title='Cod', instructions='Fry')
        self.recipe2.categories.add(self.cat)
        
        self.entry = CalendarEntry.objects.create(
            user=self.user,
            date=date.today(),
            recipe=self.recipe1,
            meal_type='dinner'
        )
        self.url = reverse('replace_calendar_recipe', kwargs={'pk': self.entry.pk})

    def test_replace_recipe_logic(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302) # Or 200 for AJAX, let's start with redirect
        
        self.entry.refresh_from_db()
        # Should be recipe2 now since it's the only other in the category
        self.assertEqual(self.entry.recipe, self.recipe2)

    def test_replace_recipe_no_other_in_category(self):
        # Remove recipe2 from category
        self.recipe2.categories.clear()
        
        response = self.client.post(self.url)
        # Should stay the same
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.recipe, self.recipe1)

    def test_replace_recipe_no_categories(self):
        # Remove all categories from recipe1
        self.recipe1.categories.clear()
        
        response = self.client.post(self.url)
        # Should stay the same
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.recipe, self.recipe1)
