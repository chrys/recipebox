from datetime import date
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from calendar_app.models import CalendarEntry
from recipes.models import Recipe

User = get_user_model()


class CalendarEntryStrTest(TestCase):
    def test_str_format(self):
        user = User.objects.create_user(username='calstr', password='pass1234!')
        recipe = Recipe.objects.create(user=user, title='Tacos', instructions='Cook')
        entry = CalendarEntry.objects.create(
            user=user, recipe=recipe, date=date(2026, 3, 15), meal_type='lunch'
        )
        self.assertEqual(str(entry), 'Tacos — 2026-03-15 (Lunch)')

    def test_str_dinner_default(self):
        user = User.objects.create_user(username='caldef', password='pass1234!')
        recipe = Recipe.objects.create(user=user, title='Pizza', instructions='Bake')
        entry = CalendarEntry.objects.create(
            user=user, recipe=recipe, date=date(2026, 1, 1)
        )
        self.assertIn('Dinner', str(entry))


class CalendarEntryUniquenessTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='caluni', password='pass1234!')
        self.recipe = Recipe.objects.create(
            user=self.user, title='Unique', instructions='Step'
        )

    def test_duplicate_entry_raises(self):
        CalendarEntry.objects.create(
            user=self.user, recipe=self.recipe,
            date=date(2026, 6, 1), meal_type='dinner'
        )
        with self.assertRaises(IntegrityError):
            CalendarEntry.objects.create(
                user=self.user, recipe=self.recipe,
                date=date(2026, 6, 1), meal_type='dinner'
            )

    def test_same_recipe_different_meal_type_ok(self):
        CalendarEntry.objects.create(
            user=self.user, recipe=self.recipe,
            date=date(2026, 6, 1), meal_type='dinner'
        )
        entry2 = CalendarEntry.objects.create(
            user=self.user, recipe=self.recipe,
            date=date(2026, 6, 1), meal_type='lunch'
        )
        self.assertEqual(entry2.meal_type, 'lunch')

    def test_same_recipe_different_date_ok(self):
        CalendarEntry.objects.create(
            user=self.user, recipe=self.recipe,
            date=date(2026, 6, 1), meal_type='dinner'
        )
        entry2 = CalendarEntry.objects.create(
            user=self.user, recipe=self.recipe,
            date=date(2026, 6, 2), meal_type='dinner'
        )
        self.assertEqual(entry2.date, date(2026, 6, 2))


class CalendarEntryOrderingTest(TestCase):
    def test_ordered_by_date_then_meal_type(self):
        user = User.objects.create_user(username='calord', password='pass1234!')
        r = Recipe.objects.create(user=user, title='R', instructions='S')
        CalendarEntry.objects.create(user=user, recipe=r, date=date(2026, 3, 2), meal_type='dinner')
        CalendarEntry.objects.create(user=user, recipe=r, date=date(2026, 3, 1), meal_type='lunch')
        CalendarEntry.objects.create(user=user, recipe=r, date=date(2026, 3, 1), meal_type='breakfast')
        entries = list(CalendarEntry.objects.filter(user=user))
        dates = [(e.date, e.meal_type) for e in entries]
        self.assertEqual(dates[0], (date(2026, 3, 1), 'breakfast'))
        self.assertEqual(dates[1], (date(2026, 3, 1), 'lunch'))
        self.assertEqual(dates[2], (date(2026, 3, 2), 'dinner'))


class CalendarEntryCascadeDeleteTest(TestCase):
    def test_deleting_recipe_deletes_entries(self):
        user = User.objects.create_user(username='calcasc', password='pass1234!')
        recipe = Recipe.objects.create(user=user, title='Gone', instructions='S')
        CalendarEntry.objects.create(user=user, recipe=recipe, date=date(2026, 1, 1))
        CalendarEntry.objects.create(user=user, recipe=recipe, date=date(2026, 1, 2))
        self.assertEqual(CalendarEntry.objects.filter(user=user).count(), 2)
        recipe.delete()
        self.assertEqual(CalendarEntry.objects.filter(user=user).count(), 0)


class CalendarEntryMealTypeChoicesTest(TestCase):
    def test_valid_meal_types(self):
        valid = ['breakfast', 'lunch', 'dinner', 'snack']
        choice_values = [c[0] for c in CalendarEntry.MEAL_TYPE_CHOICES]
        self.assertEqual(choice_values, valid)
