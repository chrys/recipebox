from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class CalendarUITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='uiuser', password='password123')
        self.client.login(username='uiuser', password='password123')

    def test_sidebar_admin_link(self):
        response = self.client.get(reverse('calendar_view'))
        self.assertContains(response, reverse('admin_settings'))
        self.assertContains(response, 'Admin Settings')

    def test_admin_page_elements(self):
        response = self.client.get(reverse('admin_settings'))
        self.assertContains(response, 'action="%s"' % reverse('add_category'))
        self.assertContains(response, 'action="%s"' % reverse('update_schedule'))
        self.assertContains(response, '<select name="category"')

    def test_schedule_week_button_presence(self):
        response = self.client.get(reverse('calendar_view'))
        self.assertContains(response, 'Schedule Current Week')
        self.assertContains(response, 'action="%s"' % reverse('schedule_current_week'))

    def test_replace_recipe_option_presence(self):
        from recipes.models import Recipe
        from calendar_app.models import CalendarEntry
        from datetime import date
        
        recipe = Recipe.objects.create(user=self.user, title='UI Recipe', instructions='Step 1')
        entry = CalendarEntry.objects.create(user=self.user, date=date.today(), recipe=recipe, meal_type='dinner')
        
        response = self.client.get(reverse('calendar_view'))
        self.assertContains(response, 'Replace Recipe')
        self.assertContains(response, reverse('replace_calendar_recipe', kwargs={'pk': entry.pk}))
