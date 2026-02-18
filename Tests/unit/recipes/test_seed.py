from django.test import TestCase
from recipes.models import Recipe, Category

class SeedDataTest(TestCase):
    def test_recipes_seeded(self):
        # We need to run the command in the test database
        from django.core.management import call_command
        call_command('seed_recipes')
        
        self.assertEqual(Recipe.objects.count(), 25)
        self.assertGreaterEqual(Category.objects.count(), 5)
        
        for cat_name in ['Meat', 'Beans', 'Fish', 'Chicken', 'Pasta']:
            cat = Category.objects.get(name=cat_name)
            self.assertEqual(cat.recipes.count(), 5)
            self.assertTrue(all(r.public for r in cat.recipes.all()))
