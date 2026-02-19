from django.db import migrations
import re
from decimal import Decimal

def parse_quantity(quantity_str):
    if not quantity_str:
        return None, ''
    
    match = re.match(r'^([\d\.]+)\s*(.*)$', quantity_str.strip())
    if not match:
        return None, ''
    
    val_str, unit_str = match.groups()
    try:
        val = Decimal(val_str)
    except:
        return None, ''
    
    unit_str = unit_str.lower().strip()
    
    unit_map = {
        'grams': 'grams',
        'gram': 'grams',
        'g': 'grams',
        'kilograms': 'kilograms',
        'kilogram': 'kilograms',
        'kg': 'kilograms',
        'cups': 'cups',
        'cup': 'cups',
        'tsp': 'tsp',
        'teaspoon': 'tsp',
        'teaspoons': 'tsp',
        'tbsp': 'tbsp',
        'tablespoon': 'tbsp',
        'tablespoons': 'tbsp',
        'piece': 'piece',
        'pieces': 'piece',
    }
    
    unit = unit_map.get(unit_str, '')
    return val, unit

def migrate_quantities(apps, schema_editor):
    RecipeIngredient = apps.get_model('recipes', 'RecipeIngredient')
    for ing in RecipeIngredient.objects.all():
        if ing.quantity and (not ing.quantity_value):
            val, unit = parse_quantity(ing.quantity)
            if val is not None:
                ing.quantity_value = val
                ing.quantity_unit = unit
                ing.save()

def reverse_migrate_quantities(apps, schema_editor):
    # No need to do anything as we kept the original 'quantity' field
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0007_recipeingredient_quantity_unit_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_quantities, reverse_migrate_quantities),
    ]
