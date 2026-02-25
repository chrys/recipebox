# Track Specification: Recipe UX Fixes & New Creation Modes

## Overview

This track addresses a set of bug fixes and UX improvements to the recipe management
experience, along with two significant new features: ingredient autocomplete with
historical data and multiple recipe creation modes (form, free text, URL scraping).

**Type:** Mixed (Bug Fixes + Features)
**Source:** Design/Feb-26/feb4/feb4.md

---

## Functional Requirements

### 1. Recipe Page Bug Fixes

**1.1 — Remove empty bullet points in ingredient list (View & Edit)**
- The recipe detail page shows two trailing empty bullet points in the ingredient list.
- Remove any empty `<li>` elements rendered for blank/empty ingredient formset rows.

**1.2 — Remove decimal points from ingredient quantity display**
- On the recipe detail page and edit page, quantities like `2.00` should display as `2`,
  and `0.50` as `0.5`. Trailing zeros after the decimal must be stripped.

**1.5 — Recipe photo: show full image at reduced size**
- Currently the photo is cropped and too large.
- The image must be displayed at a fixed maximum height (≤ 250px), preserving aspect
  ratio (no cropping, `object-fit: contain`), so that the photo, ingredients, and method
  are all visible without scrolling on a standard laptop screen.

### 2. Ingredient Autocomplete

**2.1 — Ingredient name autocomplete in recipe create/edit forms**
- When the user types in an ingredient name field, the system must suggest matching
  ingredient names.
- Suggestion sources (in priority order):
  1. Ingredients previously entered by the user across all their recipes (historical data).
  2. A built-in list of common ingredients.
- Suggestions must use fuzzy/stem matching so that "onion" and "onions" both surface the
  same suggestions. Ingredients are stored as-entered; normalization occurs only on lookup.
- The autocomplete must be implemented using a JSON API endpoint that the frontend queries
  as the user types (debounced).
- A new `Ingredient` master table must be maintained: each unique ingredient name entered
  by any user is persisted there, enabling cross-recipe suggestions.

### 3. My Recipes Page Improvements

**3.1 — Sort recipes alphabetically**
- The recipe list must be ordered alphabetically by title (A–Z) as the default sort.

**3.2 — Add list view toggle (thumbnail vs list)**
- Add a toggle button on the recipe list page to switch between:
  - **Grid/Thumbnail view** (current default): recipe cards with image thumbnails.
  - **List view**: only linked recipe titles, one per row, no images.
- The user's preferred view must be persisted via `localStorage`.

### 4. New Recipe Creation Modes

**4.1–4.2 — Tabbed creation interface**
- The `/recipes/new/` page must offer three tabs:
  1. **Form** — the existing recipe creation form (current `/recipes/new/` fields).
  2. **Create from text** — free-text entry with "Generate Recipe" action.
  3. **Create from link** — URL entry with "Generate Recipe" action.

**4.3 — Create from text**
- The user pastes free-form text containing ingredients and numbered steps.
- On clicking "Generate Recipe", the system applies rule-based parsing (no AI/LLM):
  - Lines matching `1.`, `2.`, `3.` (numbered) → parsed as instruction steps.
  - Remaining non-numbered lines → parsed as ingredient names.
- The parsed data is used to pre-fill the Form tab fields, allowing the user to
  review and save.
- Below the text area, an **example recipe format** is displayed as helper text
  showing the user exactly how to structure their input for correct parsing, e.g.:

  ```
  Example format:

  Chicken Stir Fry

  2 chicken breasts
  1 cup broccoli
  2 tbsp soy sauce
  1 clove garlic

  1. Heat oil in a pan over medium heat.
  2. Add chicken and cook for 5 minutes.
  3. Add vegetables and soy sauce.
  4. Stir fry for another 3 minutes and serve.
  ```

**4.4 — Create from link**
- The user enters a recipe URL and clicks "Generate Recipe".
- The system uses `recipe-scrapers` (already installed) to scrape the URL server-side.
- On success, the user is redirected to the recipe edit form pre-populated with the
  scraped title, ingredients, and instructions.
- On scraping failure (invalid URL, unsupported site), an error message is shown.

---

## Non-Functional Requirements

- All new backend logic must be covered by unit tests (>80% coverage).
- Each new feature or bug fix must have a corresponding test file added under `Tests/unit/recipes/`.
- The autocomplete API endpoint must respond in < 300ms for typical datasets.
- The view toggle must work without a page reload (pure JS).
- The tabbed interface must work without a page reload (pure JS tab switching).
- No new third-party libraries may be added beyond `recipe-scrapers` (already present).

---

## Acceptance Criteria

- [ ] Recipe detail and edit pages show no empty bullet points in the ingredient list.
- [ ] Ingredient quantities display without trailing zeros (e.g., `2` not `2.00`).
- [ ] Recipe photo is fully visible (uncropped) at ≤ 250px height on the detail page.
- [ ] Typing in any ingredient name field on create/edit shows autocomplete suggestions.
- [ ] Suggestions combine user history + fixed list using fuzzy matching.
- [ ] Recipe list is sorted A–Z by default.
- [ ] A grid/list toggle exists on the recipe list page; preference persists via localStorage.
- [ ] `/recipes/new/` shows three tabs (Form, Create from text, Create from link).
- [ ] Example recipe format is displayed below the "Create from text" text area.
- [ ] "Create from text" pre-fills the form with rule-parsed ingredients and steps.
- [ ] "Create from link" scrapes the URL and redirects to a pre-filled edit form.
- [ ] Every new feature/fix has a corresponding unit test under `Tests/unit/recipes/`.
- [ ] All new code has unit tests passing with >80% coverage.

---

## Out of Scope

- AI/LLM-based text parsing (rule-based only for 4.3).
- Automatic canonical normalization of ingredient names on save.
- Public-facing / unauthenticated scraping or creation flows.
- Bulk import of recipes.
- Changes to the shopping list, calendar, or admin settings pages.
