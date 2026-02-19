from django.test import TestCase
from django.contrib.auth import get_user_model
from recipes.models import Category, Recipe, RecipeIngredient, UserScheduleMapping

User = get_user_model()


class CategoryStrTest(TestCase):
    def test_str_returns_name(self):
        cat = Category(name='Italian')
        self.assertEqual(str(cat), 'Italian')


class CategorySlugUniquenessTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='u1', password='pass1234!')
        self.user2 = User.objects.create_user(username='u2', password='pass1234!')

    def test_same_slug_allowed_for_different_users(self):
        Category.objects.create(user=self.user1, name='Fish', slug='fish')
        cat2 = Category.objects.create(user=self.user2, name='Fish', slug='fish')
        self.assertEqual(cat2.slug, 'fish')

    def test_same_slug_same_user_raises(self):
        from django.db import IntegrityError
        Category.objects.create(user=self.user1, name='Fish', slug='fish')
        with self.assertRaises(IntegrityError):
            Category.objects.create(user=self.user1, name='Fish Duplicate', slug='fish')


class CategoryOrderingTest(TestCase):
    def test_categories_ordered_by_name(self):
        user = User.objects.create_user(username='ord', password='pass1234!')
        Category.objects.create(user=user, name='Zebra', slug='zebra')
        Category.objects.create(user=user, name='Apple', slug='apple')
        Category.objects.create(user=user, name='Mango', slug='mango')
        slugs = list(Category.objects.filter(user=user).values_list('slug', flat=True))
        self.assertEqual(slugs, ['apple', 'mango', 'zebra'])


class RecipeStrTest(TestCase):
    def test_str_returns_title(self):
        r = Recipe(title='Spaghetti Bolognese')
        self.assertEqual(str(r), 'Spaghetti Bolognese')


class RecipeGetAbsoluteUrlTest(TestCase):
    def test_absolute_url(self):
        user = User.objects.create_user(username='url', password='pass1234!')
        recipe = Recipe.objects.create(user=user, title='URL Test', instructions='Step')
        self.assertEqual(recipe.get_absolute_url(), f'/recipes/{recipe.pk}/')


class RecipeTotalTimeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='time', password='pass1234!')

    def test_both_times_set(self):
        r = Recipe(user=self.user, title='T', instructions='S', prep_time=10, cook_time=20)
        self.assertEqual(r.total_time, 30)

    def test_only_prep_time(self):
        r = Recipe(user=self.user, title='T', instructions='S', prep_time=15, cook_time=None)
        self.assertEqual(r.total_time, 15)

    def test_only_cook_time(self):
        r = Recipe(user=self.user, title='T', instructions='S', prep_time=None, cook_time=25)
        self.assertEqual(r.total_time, 25)

    def test_neither_time_set(self):
        r = Recipe(user=self.user, title='T', instructions='S', prep_time=None, cook_time=None)
        self.assertIsNone(r.total_time)

    def test_both_zero(self):
        r = Recipe(user=self.user, title='T', instructions='S', prep_time=0, cook_time=0)
        # 0 is falsy, so total_time should be None
        self.assertIsNone(r.total_time)


class RecipeInstructionStepsTest(TestCase):
    def test_multi_line_instructions(self):
        r = Recipe(title='T', instructions='Step 1\nStep 2\nStep 3')
        self.assertEqual(r.instruction_steps, ['Step 1', 'Step 2', 'Step 3'])

    def test_empty_lines_filtered(self):
        r = Recipe(title='T', instructions='Step 1\n\n\nStep 2\n')
        self.assertEqual(r.instruction_steps, ['Step 1', 'Step 2'])

    def test_blank_instructions(self):
        r = Recipe(title='T', instructions='')
        self.assertEqual(r.instruction_steps, [])

    def test_whitespace_only_lines_filtered(self):
        r = Recipe(title='T', instructions='Step 1\n   \n  Step 2  ')
        self.assertEqual(r.instruction_steps, ['Step 1', 'Step 2'])


class RecipeIngredientStrTest(TestCase):
    def test_str_with_quantity(self):
        ing = RecipeIngredient(name='Flour', quantity='2 cups')
        self.assertEqual(str(ing), '2 cups Flour')

    def test_str_without_quantity(self):
        ing = RecipeIngredient(name='Salt', quantity='')
        self.assertEqual(str(ing), 'Salt')


class RecipeIngredientCascadeDeleteTest(TestCase):
    def test_deleting_recipe_deletes_ingredients(self):
        user = User.objects.create_user(username='casc', password='pass1234!')
        recipe = Recipe.objects.create(user=user, title='Del', instructions='S')
        RecipeIngredient.objects.create(recipe=recipe, name='Egg')
        RecipeIngredient.objects.create(recipe=recipe, name='Milk')
        self.assertEqual(RecipeIngredient.objects.count(), 2)
        recipe.delete()
        self.assertEqual(RecipeIngredient.objects.count(), 0)


class RecipeIngredientOrderingTest(TestCase):
    def test_ordered_by_order_field(self):
        user = User.objects.create_user(username='ingo', password='pass1234!')
        recipe = Recipe.objects.create(user=user, title='Order', instructions='S')
        RecipeIngredient.objects.create(recipe=recipe, name='C', order=3)
        RecipeIngredient.objects.create(recipe=recipe, name='A', order=1)
        RecipeIngredient.objects.create(recipe=recipe, name='B', order=2)
        names = list(recipe.ingredients.values_list('name', flat=True))
        self.assertEqual(names, ['A', 'B', 'C'])


class UserScheduleMappingStrTest(TestCase):
    def test_str_format(self):
        user = User.objects.create_user(username='mapstr', password='pass1234!')
        cat = Category.objects.create(user=user, name='Pasta', slug='pasta')
        m = UserScheduleMapping.objects.create(user=user, day_of_week=3, category=cat)
        self.assertEqual(str(m), "mapstr's Wednesday -> Pasta")

    def test_str_with_null_category(self):
        user = User.objects.create_user(username='mapnull', password='pass1234!')
        m = UserScheduleMapping.objects.create(user=user, day_of_week=0, category=None)
        self.assertEqual(str(m), "mapnull's Sunday -> None")


class UserScheduleMappingUniquenessTest(TestCase):
    def test_same_user_same_day_raises(self):
        from django.db import IntegrityError
        user = User.objects.create_user(username='unimap', password='pass1234!')
        cat = Category.objects.create(user=user, name='A', slug='a')
        UserScheduleMapping.objects.create(user=user, day_of_week=1, category=cat)
        with self.assertRaises(IntegrityError):
            UserScheduleMapping.objects.create(user=user, day_of_week=1, category=cat)
