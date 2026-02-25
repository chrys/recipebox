from django.urls import path
from . import views

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe_list"),
    path("shopping-list/", views.shopping_list, name="shopping_list"),
    path("new/", views.RecipeCreateView.as_view(), name="recipe_create"),
    path("<int:pk>/", views.RecipeDetailView.as_view(), name="recipe_detail"),
    path("<int:pk>/edit/", views.RecipeUpdateView.as_view(), name="recipe_edit"),
    path("<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="recipe_delete"),
    path("<int:pk>/rate/", views.update_rating, name="recipe_update_rating"),
    path(
        "ingredients/autocomplete/",
        views.ingredient_autocomplete,
        name="ingredient_autocomplete",
    ),
    path("new/from-text/", views.recipe_from_text, name="recipe_from_text"),
    path("new/from-link/", views.recipe_from_link, name="recipe_from_link"),
]
