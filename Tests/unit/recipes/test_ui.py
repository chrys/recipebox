from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

class RecipeFormTemplateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser_ui', password='password123')
        self.client.login(username='testuser_ui', password='password123')

    def test_mandatory_asterisk_presence(self):
        response = self.client.get(reverse('recipe_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Title <span style="color: var(--color-danger, #d73a49);">*</span>')
        self.assertContains(response, 'Instructions <span style="color: var(--color-danger, #d73a49);">*</span>')
        self.assertContains(response, 'placeholder="Ingredient name *"')

    def test_star_rating_presence(self):
        recipe = Recipe.objects.create(
            user=self.user,
            title='Test Recipe Stars',
            instructions='Step 1',
            rating=3
        )
        # Detail view
        response = self.client.get(reverse('recipe_detail', kwargs={'pk': recipe.pk}))
        self.assertContains(response, 'class="recipe-rating"')
        self.assertContains(response, 'data-recipe-id="%d"' % recipe.pk)
        
        # List view
        response = self.client.get(reverse('recipe_list'))
        self.assertContains(response, 'class="recipe-rating"')

    def test_sidebar_shopping_list_link(self):
        response = self.client.get(reverse('recipe_list'))
        self.assertContains(response, reverse('shopping_list'))
        self.assertContains(response, 'Shopping List')

    def test_anonymous_sidebar_hides_shopping_list_link(self):
        self.client.logout()
        response = self.client.get(reverse('recipe_list'))
        self.assertNotContains(response, reverse('shopping_list'))
        self.assertNotContains(response, 'Shopping List')

    def test_public_recipes_visible_in_list(self):
        # Create a public recipe owned by another user
        other_user = User.objects.create_user(username='other', password='password123')
        Recipe.objects.create(
            user=other_user,
            title='Other User Public Recipe',
            instructions='Step 1',
            public=True
        )
        
        # Public recipes only show when recipe filter is set to 'public'
        response = self.client.get(reverse('recipe_list') + '?recipes=public')
        self.assertContains(response, 'Other User Public Recipe')
