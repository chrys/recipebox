import pytest
from django.contrib.auth.models import User
from recipes.models import Recipe
from recipes.templatetags.recipe_schema import recipe_json_ld

@pytest.mark.django_db
def test_recipe_schema_json_ld():
    user = User.objects.create(username="testuser")
    recipe = Recipe.objects.create(user=user, title="Test Recipe", description="A test description")
    schema_html = recipe_json_ld(recipe)
    assert '"@type": "Recipe"' in schema_html
    assert '"name": "Test Recipe"' in schema_html
