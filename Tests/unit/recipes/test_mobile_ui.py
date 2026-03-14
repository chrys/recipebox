from django.test import TestCase
from django.urls import reverse

class MobileBaseTemplateTest(TestCase):
    def test_viewport_meta_in_base(self):
        # Using a simple view that extends base.html
        response = self.client.get(reverse('account_login'))
        self.assertContains(response, '<meta name="viewport" content="width=device-width, initial-scale=1.0">')

    def test_viewport_meta_in_base_auth(self):
        # Using login view as it should extend base_auth.html or use the meta tag directly
        response = self.client.get(reverse('account_login'))
        self.assertContains(response, '<meta name="viewport" content="width=device-width, initial-scale=1.0">')
