# Release Notes - Feb 26 (Sprint 4)

## Summary
This sprint focused on improving the core Recipe UX with better sorting, more flexible views, and significantly reducing friction when adding new recipes via intelligent parsing and scraping.

## Key Features

### 1. Enhanced Recipe Navigation
- **Case-Insensitive Sorting:** The recipe list now uses a proper alphabetical A-Z sort regardless of capitalization (e.g., "apple" correctly comes before "Banana").
- **Grid/List View Toggle:** Users can now switch between a high-density grid view and a concise list view. Your preference is automatically saved for future visits.
- **High-Density Grid:** Increased the grid capacity to 6 columns on larger screens to maximize information density.

### 2. Intelligent Recipe Creation
- **Tabbed Creation Interface:** A new unified interface at `/recipes/new/` allows switching between manual forms and automated creation modes.
- **Create from Text:** Paste raw text (e.g., from an email or note) and the system will automatically extract the title, ingredients, and instruction steps to pre-fill the form.
- **Create from Link:** Provide a URL from popular recipe websites, and the system will scrape the ingredients and steps automatically.

### 3. Smart Autocomplete & Master Ingredients
- **Ingredient Master List:** Introduced a master ingredient table that tracks your common ingredients across all recipes.
- **Smart Autocomplete:** When adding ingredients to a recipe, the system now provides suggestions based on your personal history and common pantry staples.

### 4. Bug Fixes & Refinement
- **Zero-Value Cleanup:** Stripped unnecessary trailing zeros from ingredient quantities (e.g., "1.00" now shows as "1").
- **Ingredient Display Fixes:** Resolved issues where empty bullets would appear in the recipe detail view.
- **Photo Display Optimization:** Recipe images are now capped at a maximum height of 250px on the detail page to prevent excessive scrolling while maintaining the original aspect ratio.

## Technical Improvements
- **Automated Verification:** Added 22 new unit tests covering the new parsing and scraping logic.
- **Standards Compliance:** Refactored frontend JavaScript to strictly adhere to project style guidelines (terminating semicolons and block formatting).
