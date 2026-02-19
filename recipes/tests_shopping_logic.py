from django.test import TestCase
from decimal import Decimal
from recipes.utils import normalize_to_base

from django.urls import reverse
from recipes.models import Recipe, RecipeIngredient, Category
from calendar_app.models import CalendarEntry
from datetime import date
from django.contrib.auth import get_user_model

User = get_user_model()

class ShoppingListConsolidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.recipe1 = Recipe.objects.create(user=self.user, title='Recipe 1')
        self.recipe2 = Recipe.objects.create(user=self.user, title='Recipe 2')
        
        # 500g Flour
        RecipeIngredient.objects.create(
            recipe=self.recipe1, name='Flour', quantity_value=500, quantity_unit='grams', aisle='Baking'
        )
        # 1kg Flour
        RecipeIngredient.objects.create(
            recipe=self.recipe2, name='Flour', quantity_value=1, quantity_unit='kilograms', aisle='Baking'
        )
        # 1 cup Sugar
        RecipeIngredient.objects.create(
            recipe=self.recipe1, name='Sugar', quantity_value=1, quantity_unit='cups', aisle='Baking'
        )
        
        # Schedule both for today
        CalendarEntry.objects.create(user=self.user, recipe=self.recipe1, date=date.today(), meal_type='dinner')
        CalendarEntry.objects.create(user=self.user, recipe=self.recipe2, date=date.today(), meal_type='dinner')

    def test_shopping_list_consolidation(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('shopping_list'))
        self.assertEqual(response.status_code, 200)
        
        ingredients = response.context['ingredients_by_aisle']['Baking']
        # Should have Flour (1.5kg) and Sugar (250g)
        flour = next(i for i in ingredients if i['name'] == 'Flour')
        sugar = next(i for i in ingredients if i['name'] == 'Sugar')
        
        self.assertEqual(flour['value'], Decimal('1.5'))
        self.assertEqual(flour['unit'], 'kilograms')
        self.assertEqual(sugar['value'], Decimal('250'))
        self.assertEqual(sugar['unit'], 'grams')
