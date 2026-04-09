from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from recipes.models import Recipe, RecipeIngredient

from .forms import SignupForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('account_login')


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('recipe_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)

        draft = self.request.session.pop("guest_recipe_draft", None)
        if draft:
            recipe_data = draft.get("recipe") or {}
            ingredients_data = draft.get("ingredients") or []

            recipe = Recipe.objects.create(
                user=self.object,
                title=recipe_data.get("title", ""),
                description=recipe_data.get("description", ""),
                instructions=recipe_data.get("instructions", ""),
                prep_time=recipe_data.get("prep_time") or None,
                cook_time=recipe_data.get("cook_time") or None,
                servings=recipe_data.get("servings") or None,
                public=bool(recipe_data.get("public", False)),
            )

            for ingredient in sorted(
                ingredients_data,
                key=lambda i: i.get("order", 0),
            ):
                qty_value = ingredient.get("quantity_value")
                if qty_value in ("", None):
                    qty_value = None
                else:
                    try:
                        qty_value = Decimal(str(qty_value))
                    except (InvalidOperation, TypeError, ValueError):
                        qty_value = None

                RecipeIngredient.objects.create(
                    recipe=recipe,
                    name=(ingredient.get("name") or "").strip(),
                    quantity_value=qty_value,
                    quantity_unit=ingredient.get("quantity_unit", ""),
                    quantity=ingredient.get("quantity", ""),
                    aisle=ingredient.get("aisle", ""),
                    order=ingredient.get("order") or 0,
                )

            messages.success(
                self.request,
                f'Welcome! Your draft recipe "{recipe.title}" was saved automatically.',
            )

        return response
