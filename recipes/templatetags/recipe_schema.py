"""
Template tag for generating schema.org (JSON-LD) structured data for recipes.
Follows the https://schema.org/Recipe specification.
"""
import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def _iso_duration(minutes):
    """Convert minutes to ISO 8601 duration (e.g. PT30M, PT1H15M)."""
    if not minutes:
        return None
    hours, mins = divmod(minutes, 60)
    parts = ['PT']
    if hours:
        parts.append(f'{hours}H')
    if mins:
        parts.append(f'{mins}M')
    return ''.join(parts)


@register.simple_tag
def recipe_json_ld(recipe, request=None):
    """
    Output a <script type="application/ld+json"> block for a Recipe.

    Usage:
        {% load recipe_schema %}
        {% recipe_json_ld recipe request %}
    """
    data = {
        '@context': 'https://schema.org',
        '@type': 'Recipe',
        'name': recipe.title,
        'datePublished': recipe.created_at.isoformat(),
        'dateModified': recipe.updated_at.isoformat(),
    }

    if recipe.description:
        data['description'] = recipe.description

    if recipe.image and hasattr(recipe.image, 'url'):
        if request:
            data['image'] = request.build_absolute_uri(recipe.image.url)
        else:
            data['image'] = recipe.image.url

    # Ingredients
    ingredients = recipe.ingredients.all()
    if ingredients:
        data['recipeIngredient'] = [str(ing) for ing in ingredients]

    # Instructions
    steps = recipe.instruction_steps
    if steps:
        data['recipeInstructions'] = [
            {
                '@type': 'HowToStep',
                'position': i + 1,
                'text': step,
            }
            for i, step in enumerate(steps)
        ]

    # Times
    if recipe.prep_time:
        data['prepTime'] = _iso_duration(recipe.prep_time)
    if recipe.cook_time:
        data['cookTime'] = _iso_duration(recipe.cook_time)
    if recipe.total_time:
        data['totalTime'] = _iso_duration(recipe.total_time)

    # Servings
    if recipe.servings:
        data['recipeYield'] = str(recipe.servings)

    # Categories
    cat_names = [cat.name for cat in recipe.categories.all()]
    if cat_names:
        data['recipeCategory'] = cat_names[0] if len(cat_names) == 1 else cat_names

    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    return mark_safe(
        f'<script type="application/ld+json">\n{json_str}\n</script>'
    )


@register.simple_tag
def recipe_list_json_ld(recipes, request=None):
    """
    Output an ItemList JSON-LD for a list of recipes.

    Usage:
        {% load recipe_schema %}
        {% recipe_list_json_ld recipes request %}
    """
    items = []
    for i, recipe in enumerate(recipes):
        item = {
            '@type': 'ListItem',
            'position': i + 1,
            'name': recipe.title,
        }
        if request:
            item['url'] = request.build_absolute_uri(recipe.get_absolute_url())
        else:
            item['url'] = recipe.get_absolute_url()
        items.append(item)

    data = {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'name': 'My Recipes',
        'itemListElement': items,
    }

    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    return mark_safe(
        f'<script type="application/ld+json">\n{json_str}\n</script>'
    )
