import re
from decimal import Decimal


def parse_quantity(quantity_str):
    """Extract numeric value and unit from a string (e.g. '500 grams')."""
    if not quantity_str:
        return None, ""

    # regex to match "number unit"
    match = re.match(r"^([\d\.]+)\s*(.*)$", quantity_str.strip())
    if not match:
        return None, ""

    val_str, unit_str = match.groups()
    try:
        val = Decimal(val_str)
    except:
        return None, ""

    unit_str = unit_str.lower().strip()

    # Map common strings to choices
    unit_map = {
        "grams": "grams",
        "gram": "grams",
        "g": "grams",
        "kilograms": "kilograms",
        "kilogram": "kilograms",
        "kg": "kilograms",
        "cups": "cups",
        "cup": "cups",
        "tsp": "tsp",
        "teaspoon": "tsp",
        "teaspoons": "tsp",
        "tbsp": "tbsp",
        "tablespoon": "tbsp",
        "tablespoons": "tbsp",
        "piece": "piece",
        "pieces": "piece",
    }

    unit = unit_map.get(unit_str, "")
    return val, unit


def normalize_to_base(value, unit):
    """Normalize quantities to base units (grams or piece) for calculation."""
    if value is None:
        return None, ""

    if unit == "kilograms":
        return value * Decimal("1000"), "grams"
    if unit == "cups":
        return value * Decimal("250"), "grams"
    if unit in ["grams", "piece"]:
        return value, unit

    # tsp and tbsp are volume, but without density we can't easily convert to grams.
    # For now, keep them as is and consolidate only if units match.
    return value, unit


def format_quantity(value, unit):
    """Format quantities for readable display (e.g., convert grams to kilograms if >= 1000)."""
    if value is None:
        return None, ""

    if unit == "grams" and value >= 1000:
        return (value / Decimal("1000")).normalize(), "kilograms"

    if isinstance(value, Decimal):
        return value.normalize(), unit

    return value, unit


def parse_recipe_text(text: str) -> dict:
    """
    Extract ingredients (non-numbered lines) and steps (numbered lines) from text.
    Steps are expected to be prefixed with numbers (e.g., '1. ', '2) ').
    """
    ingredients = []
    steps = []
    lines = text.strip().split("\n")

    # Match lines starting with "1. ", "1) ", "2. ", etc.
    step_pattern = re.compile(r"^\d+[\.\)]\s*(.*)$")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = step_pattern.match(line)
        if match:
            steps.append(match.group(1).strip())
        else:
            ingredients.append(line)

    return {"ingredients": ingredients, "steps": steps}


COMMON_INGREDIENTS = [
    "Salt",
    "Black pepper",
    "Olive oil",
    "Butter",
    "Garlic",
    "Onion",
    "Sugar",
    "Flour",
    "Egg",
    "Milk",
    "Water",
    "Lemon",
    "Chicken breast",
    "Ground beef",
    "Rice",
    "Pasta",
    "Tomato",
    "Carrot",
    "Potato",
    "Bell pepper",
    "Cumin",
    "Paprika",
    "Oregano",
    "Basil",
    "Soy sauce",
    "Vinegar",
    "Honey",
    "Cinnamon",
    "Vanilla extract",
    "Baking powder",
]
