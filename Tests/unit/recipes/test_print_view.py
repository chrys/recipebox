import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from recipes.models import Recipe

@pytest.mark.django_db
def test_print_button_exists(client):
    user = User.objects.create(username="testuser")
    recipe = Recipe.objects.create(user=user, title="Printable Recipe")
    
    client.force_login(user)
    response = client.get(reverse('recipe_detail', kwargs={'pk': recipe.pk}))
    assert response.status_code == 200
    assert 'Print' in response.content.decode()
