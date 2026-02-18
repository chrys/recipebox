from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)
import json
from .models import Recipe, Category
from .forms import RecipeForm, RecipeIngredientFormSet


from datetime import date
from calendar_app.models import CalendarEntry
from collections import defaultdict

@login_required
def shopping_list(request):
    """Aggregate ingredients for recipes scheduled from today onwards."""
    today = date.today()
    entries = CalendarEntry.objects.filter(
        user=request.user,
        date__gte=today
    ).select_related('recipe').prefetch_related('recipe__ingredients')
    
    ingredients_by_aisle = defaultdict(list)
    
    # Track unique ingredients to combine quantities if they are the same name in the same aisle
    # For now, let's keep it simple and just group them.
    for entry in entries:
        for ing in entry.recipe.ingredients.all():
            aisle = ing.aisle or 'General'
            ingredients_by_aisle[aisle].append({
                'name': ing.name,
                'quantity': ing.quantity,
                'recipe': entry.recipe.title
            })
            
    # Sort aisles alphabetically
    sorted_ingredients = dict(sorted(ingredients_by_aisle.items()))
    
    context = {
        'ingredients_by_aisle': sorted_ingredients,
    }
    return render(request, 'recipes/shopping_list.html', context)


@login_required
@require_POST
def update_rating(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    try:
        data = json.loads(request.body)
        rating = int(data.get('rating'))
        if 1 <= rating <= 5:
            recipe.rating = rating
            recipe.save(update_fields=['rating'])
            return JsonResponse({'status': 'ok', 'rating': recipe.rating})
        else:
            return JsonResponse({'error': 'Invalid rating'}, status=400)
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid data'}, status=400)


class RecipeOwnerMixin(UserPassesTestMixin):
    """Allow access to the recipe owner; also allow any logged-in user for public recipes."""
    def test_func(self):
        recipe = self.get_object()
        return recipe.user == self.request.user or recipe.public


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12

    def get_queryset(self):
        qs = Recipe.objects.filter(user=self.request.user)
        q = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category', '').strip()

        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(description__icontains=q)
                | Q(ingredients__name__icontains=q)
            ).distinct()

        if category:
            qs = qs.filter(categories__slug=category)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        ctx['current_category'] = self.request.GET.get('category', '')
        ctx['categories'] = Category.objects.all()
        return ctx


class RecipeDetailView(LoginRequiredMixin, RecipeOwnerMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['formset'] = RecipeIngredientFormSet(self.request.POST)
        else:
            ctx['formset'] = RecipeIngredientFormSet()
        ctx['is_edit'] = False
        return ctx

    def form_valid(self, form):
        form.instance.user = self.request.user
        ctx = self.get_context_data()
        formset = ctx['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            # Set ingredient order
            for i, ingredient in enumerate(self.object.ingredients.all()):
                ingredient.order = i
                ingredient.save(update_fields=['order'])
            messages.success(self.request, f'Recipe "{self.object.title}" created!')
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class RecipeUpdateView(LoginRequiredMixin, RecipeOwnerMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['formset'] = RecipeIngredientFormSet(
                self.request.POST, instance=self.object
            )
        else:
            ctx['formset'] = RecipeIngredientFormSet(instance=self.object)
        ctx['is_edit'] = True
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        formset = ctx['formset']
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
    success_url = reverse_lazy('recipe_list')

    def form_valid(self, form):
        messages.success(self.request, f'Recipe "{self.object.title}" deleted.')
        return super().form_valid(form)
