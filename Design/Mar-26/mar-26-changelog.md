# RecipeBox Changelog - March 26, 2026

## Bug Fixes

### 🔧 Fixed: Cannot Add Public Recipes to Calendar
**Issue**: Users received "Could not add to calendar, check the form" error when trying to add public recipes from other users to their calendar.

**Root Cause**: `CalendarEntryForm` filtered recipe queryset to only show user-owned recipes, excluding public recipes.

**Solution**: Updated [calendar_app/forms.py](calendar_app/forms.py) to allow both user's own recipes and public recipes:
```python
self.fields['recipe'].queryset = Recipe.objects.filter(
    Q(user=user) | Q(public=True)
)
```

**Tests**: Added comprehensive regression test suite at [Tests/regression/test_calendar_add_public_recipe.py](Tests/regression/test_calendar_add_public_recipe.py) with 6 test cases covering:
- User can add their own recipes
- User can add other users' public recipes
- User cannot add other users' private recipes
- Form validation passes for public recipes
- Database persistence works correctly

---

## Features

### 🎯 Recipe List View Changes
**Changed**: Default recipe list now shows only user's own recipes instead of mixing own + public recipes.

**Why**: Better privacy and cleaner UX - users see their personal collection by default.

**Updated Files**:
- [recipes/views.py](recipes/views.py) - Modified `RecipeListView.get_queryset()`
- Removed `Q(public=True)` from default view

---

### ✨ New: Recipe Filter Dropdown
**Added**: Dropdown menu on `/recipes/` page to toggle between recipe sources.

**Options**:
1. **My own recipes** (default) - Shows only recipes you created
2. **Public recipes** - Shows publicly shared recipes from all users

**Implementation**:
- [recipes/views.py](recipes/views.py) - Added `recipe_filter` parameter handling
- [recipes/templates/recipes/recipe_list.html](recipes/templates/recipes/recipe_list.html) - Added filter dropdown in search/filter form
- Filter persists when searching or filtering by category

**Example Usage**:
- `?recipes=own` - Show own recipes
- `?recipes=public` - Show public recipes
- `?recipes=public&q=pasta` - Search public recipes for "pasta"

---

## Tests

### Updated Tests
- [Tests/unit/recipes/test_views.py](Tests/unit/recipes/test_views.py) - Updated 2 tests in `RecipeListViewTest`:
  - `test_public_recipes_visible` - Now requires `?recipes=public` parameter
  - `test_empty_search_returns_all` - Updated to reflect default "own recipes only" behavior

- [Tests/unit/recipes/test_ui.py](Tests/unit/recipes/test_ui.py) - Updated 1 test in `RecipeFormTemplateTest`:
  - `test_public_recipes_visible_in_list` - Now uses `?recipes=public` parameter

### New Tests
- [Tests/regression/test_calendar_add_public_recipe.py](Tests/regression/test_calendar_add_public_recipe.py) - 6 regression tests

### Test Results
✅ All 91 recipe unit tests pass
✅ All 6 calendar regression tests pass

---

## Summary
- **Files Changed**: 5
- **Tests Added**: 6 (regression)
- **Tests Updated**: 3
- **Bug Fixes**: 1
- **Features Added**: 1
