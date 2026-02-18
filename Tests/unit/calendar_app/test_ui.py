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
