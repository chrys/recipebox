from decimal import Decimal
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def normalize_quantity(value):
    """
    Removes trailing zeros from decimal numbers.
    e.g. 2.00 -> 2, 0.50 -> 0.5
    """
    if value is None:
        return ""
    try:
        # We use str(value) to handle Decimal objects correctly
        d = Decimal(str(value)).normalize()
        # The :f format specifier prevents scientific notation
        return f"{d:f}"
    except Exception:
        return value
