from django.contrib import admin
from .models import Recipe, RecipeIngredient, Category


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3
    fields = ('order', 'name', 'quantity')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'public', 'prep_time', 'cook_time', 'created_at')
    list_filter = ('categories', 'public', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories',)
    inlines = [RecipeIngredientInline]
