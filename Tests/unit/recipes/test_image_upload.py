import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from recipes.models import Recipe

@pytest.mark.django_db
def test_image_alt_text_generation():
    user = User.objects.create(username="testuser")
    recipe = Recipe.objects.create(user=user, title="Delicious Cake")
    
    # Simulate image upload
    image_file = SimpleUploadedFile("cake.jpg", b"fake_image_content", content_type="image/jpeg")
    recipe.image = image_file
    recipe.save()
    
    # Check if alt text is set (assuming a property or a field exists, or logic to handle it)
    # The requirement is that we must ensure it exists. 
    # Since there isn't a explicit alt field, let's see how to implement this.
    # We might need to add a field or a property.
    assert recipe.image_alt_text == "Delicious Cake image"
