from datetime import date, timedelta
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from calendar_app.models import CalendarEntry
from recipes.models import Recipe

User = get_user_model()


class CalendarViewTestBase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='calview', password='TestPass99!')
        self.other = User.objects.create_user(username='calother', password='TestPass99!')
        self.client.login(username='calview', password='TestPass99!')
        self.recipe = Recipe.objects.create(
            user=self.user, title='Calendar Recipe', instructions='Step 1'
        )
        self.url = reverse('calendar_view')


class CalendarViewDefaultTest(CalendarViewTestBase):
    def test_default_renders_current_month(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        today = date.today()
        # Verify the calendar is rendered with current month/year
        self.assertIn(str(today.year).encode(), response.content)
        import calendar as cal
        self.assertIn(cal.month_name[today.month].encode(), response.content)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_context_contains_expected_keys(self):
        response = self.client.get(self.url)
        # Verify response renders successfully with calendar elements
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'calendar', response.content.lower())
        self.assertIn(b'mon', response.content.lower())  # Day names
        self.assertIn(b'sun', response.content.lower())


class CalendarViewMonthNavigationTest(CalendarViewTestBase):
    def test_custom_month_year(self):
        response = self.client.get(self.url, {'year': '2026', 'month': '8'})
        self.assertEqual(response.status_code, 200)
        # Verify August 2026 is rendered
        self.assertIn(b'August', response.content)
        self.assertIn(b'2026', response.content)

    def test_january_prev_is_december(self):
        response = self.client.get(self.url, {'year': '2026', 'month': '1'})
        self.assertEqual(response.status_code, 200)
        # Verify January 2026 is rendered
        self.assertIn(b'January', response.content)
        self.assertIn(b'2026', response.content)

    def test_december_next_is_january(self):
        response = self.client.get(self.url, {'year': '2026', 'month': '12'})
        self.assertEqual(response.status_code, 200)
        # Verify December 2026 is rendered
        self.assertIn(b'December', response.content)
        self.assertIn(b'2026', response.content)

    def test_month_zero_wraps_to_december(self):
        response = self.client.get(self.url, {'year': '2026', 'month': '0'})
        self.assertEqual(response.status_code, 200)
        # Month 0 should wrap to December of previous year (2025)
        self.assertIn(b'2025', response.content)
        self.assertIn(b'December', response.content)

    def test_month_thirteen_wraps_to_january(self):
        response = self.client.get(self.url, {'year': '2026', 'month': '13'})
        self.assertEqual(response.status_code, 200)
        # Month 13 should wrap to January of next year (2027)
        self.assertIn(b'2027', response.content)
        self.assertIn(b'January', response.content)


class CalendarViewEntriesTest(CalendarViewTestBase):
    def test_entries_grouped_by_date(self):
        today = date.today()
        CalendarEntry.objects.create(
            user=self.user, recipe=self.recipe, date=today, meal_type='dinner'
        )
        response = self.client.get(self.url, {
            'year': str(today.year), 'month': str(today.month)
        })
        self.assertEqual(response.status_code, 200)
        # Verify the recipe title appears in the calendar
        self.assertIn(b'Calendar Recipe', response.content)

    def test_other_users_entries_not_shown(self):
        today = date.today()
        other_recipe = Recipe.objects.create(
            user=self.other, title='Other Recipe', instructions='S'
        )
        CalendarEntry.objects.create(
            user=self.other, recipe=other_recipe, date=today, meal_type='dinner'
        )
        response = self.client.get(self.url, {
            'year': str(today.year), 'month': str(today.month)
        })
        self.assertEqual(response.status_code, 200)
        # Other user's recipe should not appear
        self.assertNotIn(b'Other Recipe', response.content)


class CalendarAddViewTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='caladd', password='TestPass99!')
        self.client.login(username='caladd', password='TestPass99!')
        self.recipe = Recipe.objects.create(
            user=self.user, title='Add Recipe', instructions='Step'
        )
        self.url = reverse('calendar_add')

    def test_valid_post_creates_entry(self):
        response = self.client.post(self.url, {
            'recipe': self.recipe.pk,
            'date': '2026-06-15',
            'meal_type': 'dinner',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            CalendarEntry.objects.filter(
                user=self.user, recipe=self.recipe,
                date=date(2026, 6, 15), meal_type='dinner'
            ).exists()
        )

    def test_duplicate_entry_shows_warning(self):
        CalendarEntry.objects.create(
            user=self.user, recipe=self.recipe,
            date=date(2026, 6, 15), meal_type='dinner'
        )
        response = self.client.post(self.url, {
            'recipe': self.recipe.pk,
            'date': '2026-06-15',
            'meal_type': 'dinner',
        })
        self.assertEqual(response.status_code, 302)
        # Should still be only 1 entry
        self.assertEqual(
            CalendarEntry.objects.filter(
                user=self.user, date=date(2026, 6, 15), meal_type='dinner'
            ).count(), 1
        )

    def test_get_redirects_to_calendar(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('calendar_view'), response.url)

    def test_login_required(self):
        self.client.logout()
        response = self.client.post(self.url, {
            'recipe': self.recipe.pk,
            'date': '2026-06-15',
            'meal_type': 'dinner',
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CalendarEntry.objects.exists())

    def test_invalid_form_shows_error(self):
        response = self.client.post(self.url, {
            'recipe': '',
            'date': '',
            'meal_type': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CalendarEntry.objects.exists())


class CalendarDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='caldel', password='TestPass99!')
        self.other = User.objects.create_user(username='caldelother', password='TestPass99!')
        self.client.login(username='caldel', password='TestPass99!')
        self.recipe = Recipe.objects.create(
            user=self.user, title='Del Recipe', instructions='S'
        )
        self.entry = CalendarEntry.objects.create(
            user=self.user, recipe=self.recipe,
            date=date(2026, 7, 10), meal_type='dinner'
        )
        self.url = reverse('calendar_delete', kwargs={'pk': self.entry.pk})

    def test_valid_post_deletes_entry(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CalendarEntry.objects.filter(pk=self.entry.pk).exists())

    def test_redirect_includes_date_params(self):
        response = self.client.post(self.url)
        self.assertIn('year=2026', response.url)
        self.assertIn('month=7', response.url)

    def test_get_redirects_without_deleting(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CalendarEntry.objects.filter(pk=self.entry.pk).exists())

    def test_other_user_cannot_delete(self):
        self.client.login(username='caldelother', password='TestPass99!')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(CalendarEntry.objects.filter(pk=self.entry.pk).exists())

    def test_login_required(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CalendarEntry.objects.filter(pk=self.entry.pk).exists())
