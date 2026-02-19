# Specification: Recipe and Shopping List Enhancements

## Overview
This track aims to improve the precision of recipe data entry and the intelligence of the automated shopping list. By splitting ingredient quantities into numeric and unit fields, we can enable sophisticated consolidation and conversion logic (e.g., 1 cup = 250g) in the shopping list. Additionally, recipe categories will be sorted alphabetically across the application for better usability.

## Functional Requirements

### 1. Recipe Management Enhancements
- **Split Ingredient Quantity:**
    - Update `RecipeIngredient` model (or equivalent) to split the existing quantity field into two:
        - `quantity_value`: A numeric field (Decimal).
        - `quantity_unit`: A dropdown field with the following options: `grams`, `kilograms`, `cups`, `tsp`, `tbsp`, `piece`.
    - Update Recipe creation and edition forms to reflect these changes.
    - Migrate existing data (if applicable) to the new structure.
- **Alphabetical Category Sorting:**
    - Ensure categories are sorted alphabetically in:
        - The Recipes dashboard/index page.
        - The category selection dropdown in Recipe forms.
        - The Admin settings page for category management.

### 2. Smart Shopping List Enhancements
- **Unit Conversion Logic:**
    - Implement a conversion utility to handle common translations, specifically: `1 cup = 250 grams`.
- **Ingredient Consolidation:**
    - Consolidate identical ingredients in the shopping list by summing their quantities.
    - Example: `500 grams` of Flour + `1 kilogram` of Flour = `1.5 kilograms` of Flour.
- **Readable Unit Selection:**
    - Automatically select the most readable unit for display (e.g., convert `1250 grams` to `1.25 kilograms`).
- **Countable Items:**
    - For items with the unit `piece`, sum the values as counts for identical ingredients.

## Non-Functional Requirements
- **Data Integrity:** Ensure that the migration from a single quantity field to split fields does not result in data loss.
- **Performance:** Ingredient consolidation should be efficient, especially for large meal plans.

## Acceptance Criteria
- [ ] Users can select a unit from a dropdown when adding ingredients to a recipe.
- [ ] Categories are displayed in alphabetical order in all relevant UI locations.
- [ ] The shopping list correctly sums ingredients with mixed units (e.g., grams and kilograms).
- [ ] "Cups" are correctly converted to grams (250g/cup) for consolidation purposes.
- [ ] The shopping list displays consolidated totals in the most readable unit.

## Out of Scope
- Support for Imperial units (oz, lbs) unless specifically requested later.
- Automatic conversion between volume (tbsp/tsp) and weight (grams) other than the specific "cup to grams" rule.
