from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from recipes.models import Recipe

User = get_user_model()


class RecipePhotoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="photouser", password="TestPass99!"
        )
        # Create a dummy image
        image_content = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
        self.dummy_image = SimpleUploadedFile(
            "test_image.gif", image_content, content_type="image/gif"
        )

        self.recipe = Recipe.objects.create(
            user=self.user,
            title="Photo Recipe",
            instructions="Step 1",
            image=self.dummy_image,
        )

    def test_recipe_photo_style(self):
        """
        Verify that the recipe photo has the correct styles applied.
        """
        self.client.login(username="photouser", password="TestPass99!")
        url = reverse("recipe_detail", kwargs={"pk": self.recipe.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()
        # We check for the specific attributes mentioned in the plan
        self.assertIn("max-height: 250px", content)
        self.assertIn("width: auto", content)
        self.assertIn("object-fit: contain", content)
        # Also ensure it has the recipe-hero class
        self.assertIn('class="recipe-hero"', content)
