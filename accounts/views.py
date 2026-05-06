from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import firebase_admin.auth
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from recipes.models import Recipe, RecipeIngredient

from .forms import SignupForm


class CustomLoginView(TemplateView):
    template_name = 'accounts/login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('account_login')


class SignupView(TemplateView):
    template_name = 'accounts/signup.html'

@require_POST
def firebase_login(request):
    try:
        data = json.loads(request.body)
        id_token = data.get('id_token')
        
        if not id_token:
            return JsonResponse({'error': 'No token provided'}, status=400)
            
        # Verify the token with Firebase
        decoded_token = firebase_admin.auth.verify_id_token(id_token, clock_skew_seconds=60)
        email = decoded_token.get('email')
        
        if not email:
            return JsonResponse({'error': 'No email in token'}, status=400)
            
        # Get or create the user in Django
        user, created = User.objects.get_or_create(username=email, defaults={'email': email})
        
        # Log the user in
        login(request, user)

        draft = request.session.pop("guest_recipe_draft", None)
        if draft:
            recipe_data = draft.get("recipe") or {}
            ingredients_data = draft.get("ingredients") or []

            recipe = Recipe.objects.create(
                user=user,
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
                request,
                f'Welcome! Your draft recipe "{recipe.title}" was saved automatically.',
            )
            
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
