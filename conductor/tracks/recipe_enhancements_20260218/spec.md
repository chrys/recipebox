# Track Specification: Recipe Enhancements, Admin Settings & Smart Shopping

## Overview
This track introduces several user experience improvements and new functional modules to the RecipeBox application. It focuses on making recipe management more intuitive, adding user-specific administrative controls, enhancing the calendar with automated scheduling, and introducing a smart shopping list categorized by supermarket aisles.

## Functional Requirements

### 1. Recipe Management Enhancements
- **Mandatory Field Indicators:** Update the recipe creation and edit forms to visually indicate mandatory fields (e.g., using a red asterisk `*`).
- **Validation Messages:** Implement clear, user-friendly error messages that appear when a mandatory field is missed during form submission.
- **Star Rating System:** Add a 5-star rating system to recipes.
    - Users can rate recipes from 1 to 5 stars.
    - Rating is interactive (AJAX-based) and saved immediately upon clicking a star.
- **Ingredient Aisle Categorization:** Add an "Aisle" field to the recipe ingredient model to allow users to categorize items (e.g., Produce, Dairy, Bakery).

### 2. User-Specific Admin Page
- **New Navigation:** Add an "Admin" link/page under the "Calendar" section in the navigation.
- **Category Management:**
    - Users can add and remove their own custom food categories.
- **Schedule Configuration:**
    - Users can define a weekly mapping of days (Monday-Sunday) to specific food categories.

### 3. Calendar & Scheduling Improvements
- **Schedule Current Week Button:**
    - Populates each day of the current week with a random recipe from the mapped category.
    - Enabled only if the current week is empty.
- **Replace Recipe Option:**
    - Replaces a scheduled recipe with another random recipe from the same category.

### 4. Smart Shopping List
- **New Navigation:** Add a "Shopping List" page.
- **Ingredient Aggregation:** Automatically list all ingredients for recipes scheduled from today into the future.
- **Aisle Grouping:** Group and display ingredients by their assigned supermarket aisle.

### 5. Seed Data
- Create 5 public recipes for each category: Meat, Beans, Fish, Chicken, Pasta (Total: 25).
- Include images and aisle categorization for ingredients.

## Acceptance Criteria
- [ ] Mandatory fields are marked and validated.
- [ ] Interactive 5-star rating system is functional.
- [ ] User-specific categories and schedule mapping can be managed in Admin.
- [ ] "Schedule Current Week" and "Replace Recipe" work as intended in the Calendar.
- [ ] Shopping List correctly aggregates future ingredients and groups them by aisle.
- [ ] 25 high-quality seed recipes are present in the system.

## Out of Scope
- Global system-wide category management (settings are per-user).
- Advanced scheduling algorithms beyond simple category-to-day mapping.
