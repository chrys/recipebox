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
