from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Category, UserScheduleMapping
from calendar_app.models import CalendarEntry

User = get_user_model()

class SchedulingLogicTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='scheduser', password='password123')
        self.client.login(username='scheduser', password='password123')
        
        self.cat_meat = Category.objects.create(user=self.user, name='Meat', slug='meat')
        self.cat_pasta = Category.objects.create(user=self.user, name='Pasta', slug='pasta')
        
        self.recipe_meat = Recipe.objects.create(user=self.user, title='Steak', instructions='Cook it')
        self.recipe_meat.categories.add(self.cat_meat)
        
        self.recipe_pasta = Recipe.objects.create(user=self.user, title='Penne', instructions='Boil it')
        self.recipe_pasta.categories.add(self.cat_pasta)
        
        # Map Monday (1) to Meat and Tuesday (2) to Pasta
        UserScheduleMapping.objects.create(user=self.user, day_of_week=1, category=self.cat_meat)
        UserScheduleMapping.objects.create(user=self.user, day_of_week=2, category=self.cat_pasta)

    def test_schedule_current_week_logic(self):
        url = reverse('schedule_current_week')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        
        # Determine start of current week (Monday)
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        tuesday = monday + timedelta(days=1)
        
        # Check if recipes were added
        self.assertTrue(CalendarEntry.objects.filter(user=self.user, date=monday, recipe=self.recipe_meat).exists())
        self.assertTrue(CalendarEntry.objects.filter(user=self.user, date=tuesday, recipe=self.recipe_pasta).exists())

    def test_schedule_button_disabled_if_not_empty(self):
        # Add a manual entry to the current week
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        CalendarEntry.objects.create(user=self.user, date=monday, recipe=self.recipe_meat, meal_type='dinner')
        
        # Attempting to auto-schedule should probably do nothing or warn
        url = reverse('schedule_current_week')
        response = self.client.post(url)
        # Assuming the view logic checks for emptiness and doesn't overwrite
        # We can check the count of entries for the week
        week_entries_count = CalendarEntry.objects.filter(
            user=self.user, 
            date__gte=monday, 
            date__lte=monday + timedelta(days=6)
        ).count()
        self.assertEqual(week_entries_count, 1) # Only the one we manually added

    def test_schedule_current_week_no_recipes(self):
        # Remove all recipes for this user
        Recipe.objects.filter(user=self.user).delete()
        url = reverse('schedule_current_week')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        self.assertFalse(CalendarEntry.objects.filter(user=self.user, date__gte=monday).exists())
