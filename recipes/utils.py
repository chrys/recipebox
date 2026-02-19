import re
from decimal import Decimal

def parse_quantity(quantity_str):
    # ... (existing code) ...
    return val, unit

def normalize_to_base(value, unit):
    """Normalize quantities to base units (grams or piece) for calculation."""
    if value is None:
        return None, ''
    
    if unit == 'kilograms':
        return value * Decimal('1000'), 'grams'
    if unit == 'cups':
        return value * Decimal('250'), 'grams'
    if unit in ['grams', 'piece']:
        return value, unit
    
    # tsp and tbsp are volume, but without density we can't easily convert to grams.
    # For now, keep them as is and consolidate only if units match.
    return value, unit
