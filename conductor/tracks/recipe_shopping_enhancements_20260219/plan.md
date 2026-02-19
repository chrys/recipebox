# Implementation Plan: Recipe and Shopping List Enhancements

## Phase 1: Recipe Model and Form Updates [checkpoint: f86df3f]
This phase focuses on structural changes to how ingredient quantities are stored and captured.

- [x] Task: Update `RecipeIngredient` model to split quantity into `quantity_value` and `quantity_unit` (82a464a)
    - [x] Add `quantity_value` (DecimalField) and `quantity_unit` (CharField with choices) to `RecipeIngredient` in `recipes/models.py`
    - [x] Create and run migrations
    - [x] Task: Conductor - User Manual Verification 'Model Update' (Protocol in workflow.md)
- [x] Task: Update Recipe Forms and Templates (984cefa)
    - [x] Update `RecipeIngredientForm` in `recipes/forms.py` to include the two new fields
    - [x] Update recipe create/edit templates to display the new fields side-by-side
    - [x] Task: Conductor - User Manual Verification 'Form Update' (Protocol in workflow.md)
- [x] Task: Migrate Existing Data (b934b8c)
    - [x] Write a management command or migration script to parse existing string quantities into the new fields where possible
    - [x] Task: Conductor - User Manual Verification 'Data Migration' (Protocol in workflow.md)

## Phase 2: Category Sorting [checkpoint: f86df3f]
Ensuring a consistent alphabetical order for categories across the application.

- [x] Task: Implement Alphabetical Sorting for Categories (929c928)
    - [x] Update `Category` model's default ordering in `recipes/models.py`
    - [x] Ensure forms and views respect this ordering
    - [x] Task: Conductor - User Manual Verification 'Category Sorting' (Protocol in workflow.md)

## Phase 3: Smart Shopping List Logic [checkpoint: f86df3f]
Implementing the conversion and consolidation engine for the shopping list.

- [x] Task: Implement Unit Conversion Utility (021dfee)
    - [x] Create a utility function to normalize units (e.g., convert everything to grams/pieces/base units for calculation)
    - [x] Implement the specific rule: `1 cup = 250 grams`
    - [x] Task: Conductor - User Manual Verification 'Unit Conversion' (Protocol in workflow.md)
- [x] Task: Implement Ingredient Consolidation Logic (ff118f8)
    - [x] Update the shopping list generation logic to group by ingredient name
    - [x] Sum the normalized quantities
    - [x] Task: Conductor - User Manual Verification 'Ingredient Consolidation' (Protocol in workflow.md)
- [x] Task: Implement "Readable" Unit Display (aacfb3d)
    - [x] Create a utility to format the consolidated totals (e.g., 1250g -> 1.25kg)
    - [x] Update the shopping list template to use this formatter
    - [x] Task: Conductor - User Manual Verification 'Readable Display' (Protocol in workflow.md)

## Phase 4: Final Integration and Verification [checkpoint: f86df3f]
Comprehensive testing of the entire flow.

- [x] Task: End-to-End Verification (ef9f243)
    - [x] Verify full flow: Create recipe -> Plan meal -> View consolidated shopping list
    - [x] Task: Conductor - User Manual Verification 'Final Integration' (Protocol in workflow.md)

## Phase 5: UI Refinement - Side-by-Side Detail View
Refining the recipe detail page layout for better readability on desktop.

- [x] Task: Implement Side-by-Side Ingredients and Instructions (8eaaae2)
    - [x] Remove `ot-tabs` from `recipe_detail.html`
    - [x] Implement two-column layout using responsive grid
    - [x] Update ingredient display to use new quantity fields
    - [x] Task: Conductor - User Manual Verification 'Side-by-Side View' (Protocol in workflow.md)
