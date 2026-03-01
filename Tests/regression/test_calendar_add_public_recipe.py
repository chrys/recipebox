"""
Regression test for: Cannot add public recipes from other users to calendar

Bug Description:
    When a user views a public recipe from another user and tries to add it to 
    their calendar, the form validation fails with "Could not add to calendar, 
    check the form."

Root Cause:
    CalendarEntryForm filtered recipe queryset to only user's own recipes,
    excluding public recipes from other users.

Expected Behavior:
    Users should be able to add both their own recipes AND public recipes 
    from other users to their calendar.
"""

from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from calendar_app.forms import CalendarEntryForm
from calendar_app.models import CalendarEntry
from recipes.models import Recipe

User = get_user_model()


class CalendarAddPublicRecipeRegressionTest(TestCase):
    """Test that public recipes from other users can be added to calendar."""

    def setUp(self):
        """Create two users and recipes to test with."""
        self.user1 = User.objects.create_user(username='owner', password='pass1234!')
        self.user2 = User.objects.create_user(username='guest', password='pass1234!')

        # User 1's private recipe
        self.private_recipe = Recipe.objects.create(
            user=self.user1,
            title='Private Recipe',
            instructions='Secret steps',
            public=False
        )

        # User 1's public recipe
        self.public_recipe = Recipe.objects.create(
            user=self.user1,
            title='Shared Recipe',
            instructions='Public steps',
            public=True
        )

    def test_form_includes_own_recipes(self):
        """User 2 should see their own recipes in the form."""
        user2_recipe = Recipe.objects.create(
            user=self.user2,
            title='User 2 Recipe',
            instructions='Steps',
            public=False
        )
        form = CalendarEntryForm(user=self.user2)
        qs = form.fields['recipe'].queryset
        self.assertIn(user2_recipe, qs)

    def test_form_includes_public_recipes_from_others(self):
        """User 2 should see User 1's public recipes in the form."""
        form = CalendarEntryForm(user=self.user2)
        qs = form.fields['recipe'].queryset
        self.assertIn(self.public_recipe, qs, 
                      "Public recipes from other users should be in the form queryset")

    def test_form_excludes_private_recipes_from_others(self):
        """User 2 should NOT see User 1's private recipes in the form."""
        form = CalendarEntryForm(user=self.user2)
        qs = form.fields['recipe'].queryset
        self.assertNotIn(self.private_recipe, qs,
                         "Private recipes from other users should NOT be in the form queryset")

    def test_add_public_recipe_form_validation(self):
        """Form should be valid when adding another user's public recipe."""
        form = CalendarEntryForm(user=self.user2, data={
            'recipe': self.public_recipe.pk,
            'date': '2026-06-15',
            'meal_type': 'dinner',
        })
        self.assertTrue(form.is_valid(), 
                        f"Adding public recipe from other user should be valid. Errors: {form.errors}")

    def test_add_public_recipe_to_calendar_succeeds(self):
        """User should successfully add another user's public recipe to calendar."""
        # Create a valid form
        form = CalendarEntryForm(user=self.user2, data={
            'recipe': self.public_recipe.pk,
            'date': '2026-06-15',
            'meal_type': 'dinner',
        })
        self.assertTrue(form.is_valid())

        # Save the entry
        entry = form.save(commit=False)
        entry.user = self.user2
        entry.save()

        # Verify the entry was created
        self.assertEqual(CalendarEntry.objects.count(), 1)
        saved_entry = CalendarEntry.objects.first()
        self.assertEqual(saved_entry.user, self.user2)
        self.assertEqual(saved_entry.recipe, self.public_recipe)
        self.assertEqual(saved_entry.date, date(2026, 6, 15))
        self.assertEqual(saved_entry.meal_type, 'dinner')

    def test_cannot_add_private_recipe_from_others(self):
        """Form should reject another user's private recipe."""
        form = CalendarEntryForm(user=self.user2, data={
            'recipe': self.private_recipe.pk,
            'date': '2026-06-15',
            'meal_type': 'dinner',
        })
        self.assertFalse(form.is_valid(),
                         "Private recipes from other users should be invalid")
        self.assertIn('recipe', form.errors)
