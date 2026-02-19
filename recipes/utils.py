import re
from decimal import Decimal

def parse_quantity(quantity_str):
    if not quantity_str:
        return None, ''
    
    # regex to match "number unit"
    match = re.match(r'^([\d\.]+)\s*(.*)$', quantity_str.strip())
    if not match:
        return None, ''
    
    val_str, unit_str = match.groups()
    try:
        val = Decimal(val_str)
    except:
        return None, ''
    
    unit_str = unit_str.lower().strip()
    
    # Map common strings to choices
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
