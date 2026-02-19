from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from calendar_app.forms import CalendarEntryForm
from recipes.models import Recipe

User = get_user_model()


class CalendarEntryFormValidDataTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='formuser', password='pass1234!')
        self.recipe = Recipe.objects.create(
            user=self.user, title='Form Recipe', instructions='Step'
        )

    def test_valid_form(self):
        form = CalendarEntryForm(user=self.user, data={
            'recipe': self.recipe.pk,
            'date': '2026-06-15',
            'meal_type': 'dinner',
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_all_meal_types_accepted(self):
        for meal_type in ['breakfast', 'lunch', 'dinner', 'snack']:
            form = CalendarEntryForm(user=self.user, data={
                'recipe': self.recipe.pk,
                'date': '2026-06-15',
                'meal_type': meal_type,
            })
            self.assertTrue(form.is_valid(), f'{meal_type} should be valid: {form.errors}')


class CalendarEntryFormUserFilteringTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='fuser1', password='pass1234!')
        self.user2 = User.objects.create_user(username='fuser2', password='pass1234!')
        self.recipe1 = Recipe.objects.create(
            user=self.user1, title='User1 Recipe', instructions='S'
        )
        self.recipe2 = Recipe.objects.create(
            user=self.user2, title='User2 Recipe', instructions='S'
        )

    def test_user_argument_filters_recipe_queryset(self):
        form = CalendarEntryForm(user=self.user1)
        qs = form.fields['recipe'].queryset
        self.assertIn(self.recipe1, qs)
        self.assertNotIn(self.recipe2, qs)

    def test_no_user_shows_all_recipes(self):
        form = CalendarEntryForm()
        qs = form.fields['recipe'].queryset
        self.assertIn(self.recipe1, qs)
        self.assertIn(self.recipe2, qs)

    def test_submitting_other_users_recipe_rejected(self):
        """If user filtering is active, choosing another user's recipe is invalid."""
        form = CalendarEntryForm(user=self.user1, data={
            'recipe': self.recipe2.pk,
            'date': '2026-06-15',
            'meal_type': 'dinner',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('recipe', form.errors)


class CalendarEntryFormRequiredFieldsTest(TestCase):
    def test_missing_recipe(self):
        form = CalendarEntryForm(data={
            'date': '2026-06-15',
            'meal_type': 'dinner',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('recipe', form.errors)

    def test_missing_date(self):
        user = User.objects.create_user(username='fmissing', password='pass1234!')
        recipe = Recipe.objects.create(user=user, title='R', instructions='S')
        form = CalendarEntryForm(user=user, data={
            'recipe': recipe.pk,
            'meal_type': 'dinner',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_empty_form(self):
        form = CalendarEntryForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('recipe', form.errors)
        self.assertIn('date', form.errors)


class CalendarEntryFormDateWidgetTest(TestCase):
    def test_date_widget_renders_date_input(self):
        form = CalendarEntryForm()
        rendered = str(form['date'])
        self.assertIn('type="date"', rendered)
