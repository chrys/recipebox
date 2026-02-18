# Implementation Plan: Recipe Enhancements, Admin Settings & Smart Shopping

## Phase 1: Recipe Model & UI Enhancements [checkpoint: 13f33bc]
- [x] Task: Update Recipe & Ingredient Models ac41696
    - [ ] Create `Tests/unit/recipes/test_models.py` and write failing tests for new fields.
    - [ ] Add `rating` (Integer 1-5) to `Recipe` in `recipes/models.py`.
    - [ ] Add `aisle` (CharField) to `RecipeIngredient` in `recipes/models.py`.
    - [ ] Create and run migrations.
- [x] Task: Mark Mandatory Fields in UI b7b1763
    - [ ] Update `recipes/templates/recipes/recipe_form.html` to visually mark mandatory fields.
    - [ ] Add styling for validation error messages using Oat UI classes.
- [x] Task: Implement Interactive Star Rating (AJAX) 6062c6b
    - [ ] Create `Tests/unit/recipes/test_rating_view.py` and write failing tests for the rating update logic.
    - [ ] Implement `update_rating` view in `recipes/views.py`.
    - [ ] Create Vanilla JS logic in `static/js/app.js` for AJAX rating submission.
    - [ ] Update `recipes/templates/recipes/recipe_detail.html` to include the star rating component.
- [x] Task: Update Recipe Form for Aisle Entry 7c87589
    - [ ] Create `Tests/unit/recipes/test_forms.py` and write tests for aisle field in ingredient formset.
    - [ ] Update `RecipeIngredient` formset in `recipes/forms.py` to include `aisle`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Recipe Model & UI Enhancements' (Protocol in workflow.md) 13f33bc

## Phase 2: User-Specific Admin & Category Management [checkpoint: d08ca11]
- [x] Task: Create Category & Schedule Mapping Models 8ce4407
    - [ ] Create `Tests/unit/calendar_app/test_models.py` and write tests for user-specific categories and schedule mapping.
    - [ ] Update `Category` model and create `UserScheduleMapping` in `recipes/models.py` or `calendar_app/models.py`.
    - [ ] Create and run migrations.
- [x] Task: Implement Admin View & Navigation 76c6e1d
    - [ ] Create `Tests/unit/calendar_app/test_admin_views.py` and write tests for the Admin settings page access and logic.
    - [ ] Implement `admin_settings` view in `calendar_app/views.py`.
    - [ ] Update `calendar_app/urls.py` and `templates/base.html` for navigation.
- [x] Task: Category Management & Schedule Mapping UI a7f4e30
    - [ ] Implement the UI for adding/removing categories and defining the weekly schedule in the Admin page.
- [x] Task: Conductor - User Manual Verification 'Phase 2: User-Specific Admin & Category Management' (Protocol in workflow.md) d08ca11

## Phase 3: Smart Calendar Scheduling
- [x] Task: Implement "Schedule Current Week" Logic ac167fd
    - [ ] Create `Tests/unit/calendar_app/test_scheduling.py` and write tests for the auto-scheduling algorithm.
    - [ ] Implement `schedule_current_week` view and logic.
- [x] Task: "Schedule Current Week" UI ac167fd
    - [ ] Add the button to the calendar and implement JS for conditional enabling (empty week check).
- [x] Task: Implement "Replace Recipe" Logic ac167fd
    - [ ] Create `Tests/unit/calendar_app/test_replace_logic.py` and write tests for replacing a recipe with another from the same category.
    - [ ] Implement `replace_calendar_recipe` AJAX view.
- [x] Task: "Replace Recipe" UI ac167fd
    - [ ] Update calendar context menu and implement JS for AJAX replacement.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Smart Calendar Scheduling' (Protocol in workflow.md)

## Phase 4: Shopping List Module
- [ ] Task: Implement Shopping List Logic
    - [ ] Create `Tests/unit/recipes/test_shopping_list.py` and write tests for ingredient aggregation and aisle grouping.
    - [ ] Implement the shopping list aggregation logic.
- [ ] Task: Shopping List UI
    - [ ] Create the shopping list page and template grouped by aisle.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Shopping List Module' (Protocol in workflow.md)

## Phase 5: Seed Data & Final Polish
- [ ] Task: Seed 25 Public Recipes
    - [ ] Create a management command to populate the database with the required seed recipes, categories, and images.
- [ ] Task: Final Mobile & Accessibility Audit
    - [ ] Perform a full walkthrough on mobile sizes and verify ARIA compliance for new interactive elements.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Seed Data & Final Polish' (Protocol in workflow.md)
