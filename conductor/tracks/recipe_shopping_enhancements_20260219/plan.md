# Implementation Plan: Recipe and Shopping List Enhancements

## Phase 1: Recipe Model and Form Updates
This phase focuses on structural changes to how ingredient quantities are stored and captured.

- [x] Task: Update `RecipeIngredient` model to split quantity into `quantity_value` and `quantity_unit` (82a464a)
    - [ ] Add `quantity_value` (DecimalField) and `quantity_unit` (CharField with choices) to `RecipeIngredient` in `recipes/models.py`
    - [ ] Create and run migrations
    - [ ] Task: Conductor - User Manual Verification 'Model Update' (Protocol in workflow.md)
- [x] Task: Update Recipe Forms and Templates (984cefa)
    - [ ] Update `RecipeIngredientForm` in `recipes/forms.py` to include the two new fields
    - [ ] Update recipe create/edit templates to display the new fields side-by-side
    - [ ] Task: Conductor - User Manual Verification 'Form Update' (Protocol in workflow.md)
- [ ] Task: Migrate Existing Data
    - [ ] Write a management command or migration script to parse existing string quantities into the new fields where possible
    - [ ] Task: Conductor - User Manual Verification 'Data Migration' (Protocol in workflow.md)

## Phase 2: Category Sorting
Ensuring a consistent alphabetical order for categories across the application.

- [ ] Task: Implement Alphabetical Sorting for Categories
    - [ ] Update `Category` model's default ordering in `recipes/models.py`
    - [ ] Ensure forms and views respect this ordering
    - [ ] Task: Conductor - User Manual Verification 'Category Sorting' (Protocol in workflow.md)

## Phase 3: Smart Shopping List Logic
Implementing the conversion and consolidation engine for the shopping list.

- [ ] Task: Implement Unit Conversion Utility
    - [ ] Create a utility function to normalize units (e.g., convert everything to grams/pieces/base units for calculation)
    - [ ] Implement the specific rule: `1 cup = 250 grams`
    - [ ] Task: Conductor - User Manual Verification 'Unit Conversion' (Protocol in workflow.md)
- [ ] Task: Implement Ingredient Consolidation Logic
    - [ ] Update the shopping list generation logic to group by ingredient name
    - [ ] Sum the normalized quantities
    - [ ] Task: Conductor - User Manual Verification 'Ingredient Consolidation' (Protocol in workflow.md)
- [ ] Task: Implement "Readable" Unit Display
    - [ ] Create a utility to format the consolidated totals (e.g., 1250g -> 1.25kg)
    - [ ] Update the shopping list template to use this formatter
    - [ ] Task: Conductor - User Manual Verification 'Readable Display' (Protocol in workflow.md)

## Phase 4: Final Integration and Verification
Comprehensive testing of the entire flow.

- [ ] Task: End-to-End Verification
    - [ ] Verify full flow: Create recipe -> Plan meal -> View consolidated shopping list
    - [ ] Task: Conductor - User Manual Verification 'Final Integration' (Protocol in workflow.md)
