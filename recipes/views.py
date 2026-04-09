from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
import json
from .models import Recipe, Category, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientFormSet, RecipeIngredientForm
from django.forms import inlineformset_factory
from decimal import Decimal
from recipe_scrapers import scrape_me


from datetime import date
from calendar_app.models import CalendarEntry
from collections import defaultdict

from .utils import normalize_to_base


def shopping_list(request):
    """Aggregate and consolidate ingredients for recipes scheduled from today onwards."""
    if not request.user.is_authenticated:
        return render(
            request,
            "recipes/shopping_list.html",
            {
                "ingredients_by_aisle": {},
                "guest_view": True,
            },
        )

    today = date.today()
    entries = (
        CalendarEntry.objects.filter(user=request.user, date__gte=today)
        .select_related("recipe")
        .prefetch_related("recipe__ingredients")
    )

    # Store as: { (aisle, name, unit): total_value }
    consolidated = defaultdict(Decimal)
    # Track which recipes use which ingredient (optional, but nice)
    ingredient_recipes = defaultdict(set)

    for entry in entries:
        for ing in entry.recipe.ingredients.all():
            aisle = ing.aisle or "General"
            name = ing.name.strip().title()

            val = ing.quantity_value
            unit = ing.quantity_unit

            # If new fields are missing, try to parse the old 'quantity' string
            if val is None and ing.quantity:
                from .utils import parse_quantity

                val, unit = parse_quantity(ing.quantity)

            if val is not None:
                norm_val, norm_unit = normalize_to_base(val, unit)
                consolidated[(aisle, name, norm_unit)] += norm_val
                ingredient_recipes[(aisle, name, norm_unit)].add(entry.recipe.title)
            else:
                # Handle ingredients with only text descriptions (e.g., "a pinch")
                # We'll just list these separately or group by name/unit=''
                consolidated[(aisle, name, ing.quantity)] += Decimal("0")
                ingredient_recipes[(aisle, name, ing.quantity)].add(entry.recipe.title)

    # Convert to structured data for template
    # { aisle: [ {name, value, unit, recipes}, ... ] }
    ingredients_by_aisle = defaultdict(list)
    for (aisle, name, unit), value in consolidated.items():
        from .utils import format_quantity

        display_val, display_unit = format_quantity(value, unit)

        ingredients_by_aisle[aisle].append(
            {
                "name": name,
                "value": display_val if display_val and display_val > 0 else None,
                "unit": display_unit,
                "recipes": ", ".join(sorted(ingredient_recipes[(aisle, name, unit)])),
            }
        )

    # Sort aisles alphabetically
    sorted_ingredients = dict(sorted(ingredients_by_aisle.items()))

    context = {
        "ingredients_by_aisle": sorted_ingredients,
        "guest_view": False,
    }
    return render(request, "recipes/shopping_list.html", context)


@login_required
@require_POST
def update_rating(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    try:
        data = json.loads(request.body)
        rating = int(data.get("rating"))
        if 1 <= rating <= 5:
            recipe.rating = rating
            recipe.save(update_fields=["rating"])
            return JsonResponse({"status": "ok", "rating": recipe.rating})
        else:
            return JsonResponse({"error": "Invalid rating"}, status=400)
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({"error": "Invalid data"}, status=400)


class RecipeOwnerMixin(UserPassesTestMixin):
    """Allow access only to the recipe owner."""

    def test_func(self):
        recipe = self.get_object()
        return recipe.user == self.request.user


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 12

    def get_queryset(self):
        # Determine whether to show own recipes or public recipes
        if self.request.user.is_authenticated:
            recipe_filter = self.request.GET.get("recipes", "own").strip()

            if recipe_filter == "public":
                # Show only public recipes
                qs = Recipe.objects.filter(public=True)
            else:
                # Show only recipes owned by the user (default)
                qs = Recipe.objects.filter(user=self.request.user)
        else:
            # Anonymous users can browse only public recipes
            qs = Recipe.objects.filter(public=True)

        q = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()

        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(description__icontains=q)
                | Q(ingredients__name__icontains=q)
            ).distinct()

        if category:
            qs = qs.filter(categories__slug=category)

        from django.db.models.functions import Lower

        return qs.order_by(Lower("title"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_query"] = self.request.GET.get("q", "")
        ctx["current_category"] = self.request.GET.get("category", "")
        if self.request.user.is_authenticated:
            ctx["recipe_filter"] = self.request.GET.get("recipes", "own")
        else:
            ctx["recipe_filter"] = "public"
        ctx["categories"] = Category.objects.all().order_by("name")
        return ctx


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Recipe.objects.filter(Q(public=True) | Q(user=self.request.user))
        return Recipe.objects.filter(public=True)


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"

    def get_initial(self):
        initial = super().get_initial()
        prefill = self.request.session.get("prefill_recipe")
        if prefill:
            if "instructions" in prefill:
                initial["instructions"] = prefill["instructions"]
            if "title" in prefill:
                initial["title"] = prefill["title"]
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["formset"] = RecipeIngredientFormSet(self.request.POST)
        else:
            prefill = self.request.session.pop("prefill_recipe", None)
            if prefill and "ingredients" in prefill:
                initial_ingredients = [{"name": ing} for ing in prefill["ingredients"]]
                # Use the existing formset class but pass initial data
                ctx["formset"] = RecipeIngredientFormSet(initial=initial_ingredients)
            else:
                ctx["formset"] = RecipeIngredientFormSet()
        ctx["is_edit"] = False
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        formset = ctx["formset"]
        if formset.is_valid():
            if not self.request.user.is_authenticated:
                recipe_payload = {
                    "title": form.cleaned_data.get("title", ""),
                    "description": form.cleaned_data.get("description", ""),
                    "instructions": form.cleaned_data.get("instructions", ""),
                    "prep_time": form.cleaned_data.get("prep_time"),
                    "cook_time": form.cleaned_data.get("cook_time"),
                    "servings": form.cleaned_data.get("servings"),
                    "public": form.cleaned_data.get("public", False),
                }

                ingredient_payload = []
                for ingredient_form in formset.forms:
                    cleaned = getattr(ingredient_form, "cleaned_data", None) or {}
                    if not cleaned or cleaned.get("DELETE"):
                        continue
                    name = (cleaned.get("name") or "").strip()
                    if not name:
                        continue

                    ingredient_payload.append(
                        {
                            "name": name,
                            "quantity_value": (
                                str(cleaned.get("quantity_value"))
                                if cleaned.get("quantity_value") is not None
                                else None
                            ),
                            "quantity_unit": cleaned.get("quantity_unit", ""),
                            "quantity": cleaned.get("quantity", ""),
                            "aisle": cleaned.get("aisle", ""),
                            "order": cleaned.get("order") or 0,
                        }
                    )

                self.request.session["guest_recipe_draft"] = {
                    "recipe": recipe_payload,
                    "ingredients": ingredient_payload,
                }
                self.request.session["prefill_recipe"] = {
                    "title": recipe_payload["title"],
                    "instructions": recipe_payload["instructions"],
                    "ingredients": [ing["name"] for ing in ingredient_payload],
                }
                self.request.session.modified = True

                messages.info(
                    self.request,
                    "Draft captured. Sign up to save this recipe permanently.",
                )
                return redirect("recipe_create")

            form.instance.user = self.request.user
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            # Set ingredient order
            for i, ingredient in enumerate(self.object.ingredients.all()):
                ingredient.order = i
                ingredient.save(update_fields=["order"])
            messages.success(self.request, f'Recipe "{self.object.title}" created!')
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class RecipeUpdateView(LoginRequiredMixin, RecipeOwnerMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipes/recipe_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx["formset"] = RecipeIngredientFormSet(
                self.request.POST, instance=self.object
            )
        else:
            ctx["formset"] = RecipeIngredientFormSet(instance=self.object)
        ctx["is_edit"] = True
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        formset = ctx["formset"]
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, f'Recipe "{self.object.title}" updated!')
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class RecipeDeleteView(LoginRequiredMixin, RecipeOwnerMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy("recipe_list")

    def form_valid(self, form):
        messages.success(self.request, f'Recipe "{self.object.title}" deleted.')
        return super().form_valid(form)


def ingredient_autocomplete(request):
    """Return JSON list of ingredient name suggestions for autocomplete."""
    from .models import Ingredient
    from .utils import COMMON_INGREDIENTS

    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"suggestions": []})

    # Historical ingredients for this user + global ones
    if request.user.is_authenticated:
        ingredient_qs = Ingredient.objects.filter(
            Q(user=request.user) | Q(user=None), name__icontains=query
        )
    else:
        ingredient_qs = Ingredient.objects.filter(user=None, name__icontains=query)

    db_matches = ingredient_qs.values_list("name", flat=True).distinct()

    # Built-in common ingredients
    builtin_matches = [
        name for name in COMMON_INGREDIENTS if query.lower() in name.lower()
    ]

    # Combine and unique, keeping original casing from DB if possible
    suggestions = sorted(list(set(list(db_matches) + builtin_matches)))

    return JsonResponse({"suggestions": suggestions})


@require_POST
def recipe_from_text(request):
    """Parse recipe from free-text and pre-fill create form."""
    text = request.POST.get("text", "").strip()
    if not text:
        messages.error(request, "No text provided.")
        return redirect("recipe_create")

    from .utils import parse_recipe_text

    parsed = parse_recipe_text(text)

    # Store in session for RecipeCreateView to pick up
    request.session["prefill_recipe"] = {
        "title": parsed.get("title", ""),
        "ingredients": parsed["ingredients"],
        "instructions": "\n".join(parsed["steps"]),
    }

    messages.success(
        request, "Recipe pre-filled from text! Please review and save below."
    )
    return redirect("recipe_create")


@require_POST
def recipe_from_link(request):
    """Scrape recipe from URL and pre-fill create form."""
    url = request.POST.get("url", "").strip()
    if not url:
        messages.error(request, "No URL provided.")
        return redirect("recipe_create")

    try:
        scraper = scrape_me(url)
        # Handle instructions whether they are a list or string
        instr = scraper.instructions()
        if isinstance(instr, list):
            instr = "\n".join(instr)

        # Store in session for RecipeCreateView to pick up
        request.session["prefill_recipe"] = {
            "title": scraper.title(),
            "ingredients": scraper.ingredients(),
            "instructions": instr,
        }
        messages.success(
            request, "Recipe scraped successfully! Please review and save below."
        )
    except Exception:
        messages.error(
            request,
            "Could not scrape the recipe from this link. You may need to enter it manually.",
        )
        return redirect("recipe_create")

    return redirect("recipe_create")
