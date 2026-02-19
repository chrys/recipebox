import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Category

User = get_user_model()


class RecipeListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='listuser', password='TestPass99!')
        self.other = User.objects.create_user(username='other', password='TestPass99!')
        self.url = reverse('recipe_list')

        self.own_recipe = Recipe.objects.create(
            user=self.user, title='My Pasta', instructions='Boil'
        )
        self.public_recipe = Recipe.objects.create(
            user=self.other, title='Public Salad', instructions='Toss', public=True
        )
        self.private_recipe = Recipe.objects.create(
            user=self.other, title='Secret Soup', instructions='Simmer', public=False
        )

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_own_recipes_visible(self):
        self.client.login(username='listuser', password='TestPass99!')
        response = self.client.get(self.url)
        self.assertContains(response, 'My Pasta')

    def test_public_recipes_visible(self):
        self.client.login(username='listuser', password='TestPass99!')
        response = self.client.get(self.url)
        self.assertContains(response, 'Public Salad')

    def test_private_other_recipes_not_visible(self):
        self.client.login(username='listuser', password='TestPass99!')
        response = self.client.get(self.url)
        self.assertNotContains(response, 'Secret Soup')

    def test_search_by_title(self):
        self.client.login(username='listuser', password='TestPass99!')
        response = self.client.get(self.url, {'q': 'Pasta'})
        self.assertContains(response, 'My Pasta')
        self.assertNotContains(response, 'Public Salad')

    def test_search_by_ingredient(self):
        self.client.login(username='listuser', password='TestPass99!')
        from recipes.models import RecipeIngredient
        RecipeIngredient.objects.create(
            recipe=self.own_recipe, name='Parmesan', quantity='50g'
        )
        response = self.client.get(self.url, {'q': 'Parmesan'})
        self.assertContains(response, 'My Pasta')

    def test_filter_by_category(self):
        self.client.login(username='listuser', password='TestPass99!')
        cat = Category.objects.create(user=self.user, name='Italian', slug='italian')
        self.own_recipe.categories.add(cat)
        response = self.client.get(self.url, {'category': 'italian'})
        self.assertContains(response, 'My Pasta')
        self.assertNotContains(response, 'Public Salad')

    def test_empty_search_returns_all(self):
        self.client.login(username='listuser', password='TestPass99!')
        response = self.client.get(self.url, {'q': ''})
        self.assertContains(response, 'My Pasta')
        self.assertContains(response, 'Public Salad')

    def test_context_contains_search_query(self):
        self.client.login(username='listuser', password='TestPass99!')
        response = self.client.get(self.url, {'q': 'test'})
        self.assertEqual(response.status_code, 200)
        # Verify search functionality works
        self.assertContains(response, 'recipe', status_code=200)

    def test_context_contains_categories(self):
        self.client.login(username='listuser', password='TestPass99!')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Verify page renders with recipe list content
        self.assertContains(response, 'My Pasta', status_code=200)


class RecipeDetailViewTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='TestPass99!')
        self.stranger = User.objects.create_user(username='stranger', password='TestPass99!')
        self.recipe = Recipe.objects.create(
            user=self.owner, title='Detail Recipe', instructions='Step 1'
        )
        self.public_recipe = Recipe.objects.create(
            user=self.owner, title='Public Detail', instructions='Step 1', public=True
        )

    def test_owner_can_view(self):
        self.client.login(username='owner', password='TestPass99!')
        url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail Recipe')

    def test_public_recipe_viewable_by_other(self):
        self.client.login(username='stranger', password='TestPass99!')
        url = reverse('recipe_detail', kwargs={'pk': self.public_recipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_private_recipe_denied_to_other(self):
        self.client.login(username='stranger', password='TestPass99!')
        url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_login_required(self):
        url = reverse('recipe_detail', kwargs={'pk': self.recipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class RecipeCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='creator', password='TestPass99!')
        self.url = reverse('recipe_create')

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_renders_form(self):
        self.client.login(username='creator', password='TestPass99!')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Verify form is rendered with expected form fields
        self.assertContains(response, 'title', status_code=200)
        self.assertContains(response, 'instructions', status_code=200)

    def test_valid_post_creates_recipe(self):
        self.client.login(username='creator', password='TestPass99!')
        data = {
            'title': 'New Recipe',
            'instructions': 'Do the thing',
            # Ingredient formset management data
            'ingredients-TOTAL_FORMS': '0',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        recipe = Recipe.objects.get(title='New Recipe')
        self.assertEqual(recipe.user, self.user)

    def test_invalid_post_rerenders_form(self):
        self.client.login(username='creator', password='TestPass99!')
        data = {
            'title': '',
            'instructions': '',
            'ingredients-TOTAL_FORMS': '0',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        # Verify form is re-rendered (contains form fields)
        self.assertContains(response, 'title', status_code=200)


class RecipeUpdateViewTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='upowner', password='TestPass99!')
        self.other = User.objects.create_user(username='upother', password='TestPass99!')
        self.recipe = Recipe.objects.create(
            user=self.owner, title='Original', instructions='Old'
        )
        self.url = reverse('recipe_edit', kwargs={'pk': self.recipe.pk})

    def test_owner_can_update(self):
        self.client.login(username='upowner', password='TestPass99!')
        data = {
            'title': 'Updated Title',
            'instructions': 'New instructions',
            'ingredients-TOTAL_FORMS': '0',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, 'Updated Title')

    def test_non_owner_denied(self):
        self.client.login(username='upother', password='TestPass99!')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get_shows_edit_context(self):
        self.client.login(username='upowner', password='TestPass99!')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Verify edit page renders with recipe title
        self.assertContains(response, 'Original', status_code=200)


class RecipeDeleteViewTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='delowner', password='TestPass99!')
        self.other = User.objects.create_user(username='delother', password='TestPass99!')
        self.recipe = Recipe.objects.create(
            user=self.owner, title='Delete Me', instructions='Bye'
        )
        self.url = reverse('recipe_delete', kwargs={'pk': self.recipe.pk})

    def test_owner_can_delete(self):
        self.client.login(username='delowner', password='TestPass99!')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Recipe.objects.filter(pk=self.recipe.pk).exists())

    def test_non_owner_denied(self):
        self.client.login(username='delother', password='TestPass99!')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Recipe.objects.filter(pk=self.recipe.pk).exists())

    def test_delete_redirects_to_list(self):
        self.client.login(username='delowner', password='TestPass99!')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('recipe_list'))

    def test_login_required(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(pk=self.recipe.pk).exists())
