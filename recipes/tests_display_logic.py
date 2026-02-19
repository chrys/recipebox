from django.test import TestCase
from decimal import Decimal
from recipes.utils import normalize_to_base, format_quantity

class ShoppingListDisplayTest(TestCase):
    def test_format_grams_to_kilograms(self):
        val, unit = format_quantity(Decimal('1500'), 'grams')
        self.assertEqual(val, Decimal('1.5'))
        self.assertEqual(unit, 'kilograms')

    def test_format_small_grams(self):
        val, unit = format_quantity(Decimal('500'), 'grams')
        self.assertEqual(val, Decimal('500'))
        self.assertEqual(unit, 'grams')

    def test_format_pieces(self):
        val, unit = format_quantity(Decimal('3'), 'piece')
        self.assertEqual(val, Decimal('3'))
        self.assertEqual(unit, 'piece')
