# Implementation Plan: Recipe UX Fixes & New Creation Modes

## Phase 1: Bug Fixes — Recipe Display [checkpoint: 71887c6]

- [x] Task: Fix empty bullet points in ingredient list a3d5336
- [x] Task: Strip trailing zeros from quantity display a3d5336
- [x] Task: Fix recipe photo display (full image, max 250px height) e6bd869
    - [ ] Write failing test in `Tests/unit/recipes/test_recipe_photo.py` asserting the `<img>` element has the correct CSS class/style on the detail page
    - [ ] Update `recipe_detail.html` image element: set `max-height: 250px; width: auto; object-fit: contain`
    - [ ] Run tests and confirm green
    - [ ] Commit

- [ ] Task: Conductor - User Manual Verification 'Phase 1: Bug Fixes' (Protocol in workflow.md)

---

## Phase 2: Ingredient Autocomplete [checkpoint: 1fcb791]

- [x] Task: Create `Ingredient` master model and migration 4c4685d
    - [ ] Write failing test in `Tests/unit/recipes/test_ingredient_autocomplete.py` asserting `Ingredient` model exists with `name` field and `user` FK
    - [ ] Add `Ingredient` model to `recipes/models.py` with fields: `user` (FK, nullable for global), `name` (CharField, unique per user), `created_at`
    - [ ] Generate and run migration
    - [ ] Run tests and confirm green
    - [ ] Commit

- [x] Task: Auto-persist ingredient names on recipe save d3497f1
    - [ ] Write failing test asserting that saving a `RecipeIngredient` upserts into the `Ingredient` master table for that user
    - [ ] Override `save()` on `RecipeIngredient` or use a `post_save` signal to upsert ingredient name into `Ingredient` table
    - [ ] Run tests and confirm green
    - [ ] Commit

- [x] Task: Build ingredient autocomplete API endpoint e84cea1
    - [ ] Write failing test in `Tests/unit/recipes/test_ingredient_autocomplete.py` asserting the endpoint returns JSON suggestions combining user history + fixed list, filtered by query, using fuzzy/stem matching
    - [ ] Add `ingredient_autocomplete` view to `recipes/views.py`: accepts `?q=` param, queries `Ingredient` table for user's history + common list, returns JSON `{suggestions: [...]}`
    - [ ] Add built-in common ingredients list (constant in `recipes/utils.py`)
    - [ ] Add URL pattern `/recipes/ingredients/autocomplete/` in `recipes/urls.py`
    - [ ] Run tests and confirm green
    - [ ] Commit

- [x] Task: Wire autocomplete to ingredient name fields in create/edit form 3d844c2
    - [ ] Write failing test in `Tests/unit/recipes/test_ingredient_autocomplete.py` asserting the ingredient name input has the correct `data-autocomplete-url` attribute in the rendered form
    - [ ] Update `recipe_form.html` ingredient name inputs: add `data-autocomplete-url` attribute
    - [ ] Add vanilla JS autocomplete widget (debounced fetch → dropdown) in a new `static/js/ingredient_autocomplete.js`
    - [ ] Run tests and confirm green
    - [ ] Commit

- [ ] Task: Conductor - User Manual Verification 'Phase 2: Ingredient Autocomplete' (Protocol in workflow.md)

---

## Phase 3: Recipe List Improvements

- [x] Task: Sort recipe list alphabetically by title 0516968
    - [ ] Write failing test in `Tests/unit/recipes/test_recipe_list.py` asserting recipes are returned in A–Z order by title
    - [ ] Update `RecipeListView.get_queryset()` to order by `title` (override `Recipe.Meta.ordering`)
    - [ ] Run tests and confirm green
    - [ ] Commit

- [x] Task: Add grid/list view toggle with localStorage persistence 2699635
    - [x] Write failing test in `Tests/unit/recipes/test_recipe_list.py` asserting the toggle button and list-view container are present in the rendered template
    - [x] Update `recipe_list.html`: add toggle button, add list-view HTML block (linked titles only), add CSS classes for grid/list states
    - [x] Add vanilla JS in `static/js/recipe_list_toggle.js`: toggle CSS class on container, persist choice to `localStorage`, restore on page load
    - [x] Run tests and confirm green
    - [x] Commit

- [ ] Task: Conductor - User Manual Verification 'Phase 3: Recipe List Improvements' (Protocol in workflow.md)

---

## Phase 4: New Recipe Creation Modes

- [ ] Task: Add tabbed interface to `/recipes/new/` page
    - [ ] Write failing test in `Tests/unit/recipes/test_recipe_create_modes.py` asserting all three tab labels (Form, Create from text, Create from link) are present in the rendered template
    - [ ] Update `recipe_form.html` (or create new `recipe_create_tabs.html`): add tab nav and three tab panels; the Form tab wraps the existing form
    - [ ] Add vanilla JS tab switching (no page reload)
    - [ ] Only show tabs on create (not edit): use existing `is_edit` context flag
    - [ ] Run tests and confirm green
    - [ ] Commit

- [ ] Task: Implement "Create from text" parsing and pre-fill
    - [ ] Write failing test in `Tests/unit/recipes/test_recipe_create_modes.py` asserting the `parse_recipe_text()` utility correctly extracts ingredients (non-numbered lines) and steps (numbered lines) from sample text
    - [ ] Add `parse_recipe_text(text: str) -> dict` function to `recipes/utils.py`
    - [ ] Add `recipe_from_text` POST view to `recipes/views.py`: calls `parse_recipe_text`, redirects to create form pre-filled via GET params or session
    - [ ] Add URL pattern `/recipes/new/from-text/` in `recipes/urls.py`
    - [ ] Update "Create from text" tab panel: text area + example format hint + "Generate Recipe" button posting to the new view
    - [ ] Run tests and confirm green
    - [ ] Commit

- [ ] Task: Implement "Create from link" scraping and pre-fill
    - [ ] Write failing test in `Tests/unit/recipes/test_recipe_create_modes.py` asserting the `recipe_from_link` view returns a redirect with scraped data pre-filled (mock `scrape_me`) and returns an error on scraping failure
    - [ ] Add `recipe_from_link` POST view to `recipes/views.py`: accepts URL, calls `scrape_me()`, stores result in session, redirects to create form; handles `scrape_me` exceptions gracefully
    - [ ] Add URL pattern `/recipes/new/from-link/` in `recipes/urls.py`
    - [ ] Update "Create from link" tab panel: URL input + "Generate Recipe" button
    - [ ] Update `RecipeCreateView` to read pre-fill data from session when present
    - [ ] Run tests and confirm green
    - [ ] Commit

- [ ] Task: Conductor - User Manual Verification 'Phase 4: New Creation Modes' (Protocol in workflow.md)
