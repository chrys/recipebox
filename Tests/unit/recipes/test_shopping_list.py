from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe, RecipeIngredient
from calendar_app.models import CalendarEntry

User = get_user_model()

class ShoppingListLogicTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='shopuser', password='password123')
        self.client.login(username='shopuser', password='password123')
        
        self.recipe = Recipe.objects.create(user=self.user, title='Shopping Recipe', instructions='Step 1')
        self.ing1 = RecipeIngredient.objects.create(recipe=self.recipe, name='Milk', quantity='1L', aisle='Dairy')
        self.ing2 = RecipeIngredient.objects.create(recipe=self.recipe, name='Bread', quantity='1 loaf', aisle='Bakery')
        
        # Schedule for today
        CalendarEntry.objects.create(user=self.user, date=date.today(), recipe=self.recipe, meal_type='dinner')
        
        # Schedule for past (should NOT be included)
        self.past_recipe = Recipe.objects.create(user=self.user, title='Past Recipe', instructions='Step 1')
        RecipeIngredient.objects.create(recipe=self.past_recipe, name='Old Egg', quantity='1', aisle='Dairy')
        CalendarEntry.objects.create(user=self.user, date=date.today() - timedelta(days=1), recipe=self.past_recipe, meal_type='dinner')

        self.url = reverse('shopping_list')

    def test_shopping_list_view_accessible(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Verify the response contains ingredients
        self.assertIn(b'Milk', response.content)
        self.assertIn(b'Bread', response.content)

    def test_shopping_list_aggregation(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        # Verify Dairy and Bakery sections are present
        self.assertIn(b'Dairy', response.content)
        self.assertIn(b'Bakery', response.content)
        
        # Verify Milk is in the response (Dairy aisle)
        self.assertIn(b'Milk', response.content)
        
        # Verify Bread is in the response (Bakery aisle)
        self.assertIn(b'Bread', response.content)
        
        # Verify past recipe's ingredient is NOT in the response
        self.assertNotIn(b'Old Egg', response.content)

    def test_shopping_list_guest_view_is_accessible(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign up to save and manage your shopping list.', response.content)
        self.assertNotIn(b'Milk', response.content)
