# Product Requirements Document (PRD): Mobile-Friendly RecipeBox

## 1. Project Overview
**Goal:** Make the newly developed RecipeBox application (hosted at `https://www.fasolaki.com/recipes/`) fully responsive and mobile-friendly. 
**Context:** Current web app covers recipe management, daily calendar planning, shopping lists, and authentication. Many users cook with their smartphones in the kitchen, making a seamless mobile experience critical to user retention and satisfaction.

## 2. Target Audience
- Home cooks utilizing their smartphones/tablets in the kitchen for following recipes.
- Users planning meals on-the-go via the calendar module.
- Users consulting their shopping lists while at the grocery store.

## 3. Scope of Work
This effort focuses on the **front-end presentation layer** (HTML templates and CSS). No backend logic changes are required unless specific API behaviors limit mobile capabilities.

The key views requiring optimization are:
- **Authentication:** Login (`login.html`) and Sign Up (`signup.html`)
- **Recipes:** Grid/List (`recipe_list.html`), Detail view (`recipe_detail.html`), and Form (`recipe_form.html`)
- **Calendar App:** Main calendar board (`calendar.html`) and settings (`admin_settings.html`)
- **Shopping List:** List view (`shopping_list.html`)

## 4. Functional Requirements & UX/UI Specifications

### 4.1 Global Layout & Navigation
- **Viewport Meta:** Ensure `<meta name="viewport" content="width=device-width, initial-scale=1.0">` is present in `templates/base.html` and `templates/base_auth.html`.
- **Navigation Menu:** 
  - Switch from a horizontal header layout to a **Hamburger Menu** on screens `< 768px`.
  - Fix the navigation bar to the top (`position: sticky` or `fixed`) for easy access while scrolling through long recipes.
- **Touch Targets:** Minimum sizes for all interactive elements (buttons, links, form inputs) must be at least `44x44px` to meet mobile accessibility guidelines.
- **Typography:** Ensure font sizes scale appropriately (using `rem` units). Body text should be legible without zooming (min `16px`).

### 4.2 Recipe Module
- **Recipe Grid (`recipe_list.html`):**
  - Desktop: 3-4 columns.
  - Tablet (`max-width: 1024px`): 2 columns.
  - Mobile (`max-width: 768px`): 1 column grid layout.
  - Ensure recipe thumbnail images span 100% of their container width (`max-width: 100%; height: auto;`).
- **Recipe Details (`recipe_detail.html`):**
  - Content should stack vertically.
  - Images, ingredient lists, and instructions should use full viewport width with appropriate side padding (e.g., `1rem`).
  - Eliminate any horizontal scrolling (apply `overflow-x: hidden` to the main wrapper cautiously).
- **Recipe Form (`recipe_form.html`):**
  - Input fields, textareas, and select dropdowns must be `width: 100%` on mobile.

### 4.3 Calendar Module
- **Calendar Grid (`calendar.html`):**
  - A traditional 7-column calendar is too cramped on mobile screens. Implement a media query to adjust the view.
  - On viewports `< 768px`, transition the CSS grid from a monthly/weekly tabular format to a **stacked daily list format** or introduce a horizontal scrolling container (`overflow-x: auto; scroll-snap-type: x mandatory;`) for the days.
  - Ensure empty state messages adapt to smaller screens without breaking layout.

### 4.4 Shopping List
- **List View (`shopping_list.html`):**
  - Optimize the list items for one-handed use at the grocery store.
  - Ensure checkboxes and delete/edit action buttons are large and spaced out to prevent accidental taps.

## 5. Technical Requirements
- Use standard CSS media queries (e.g., `@media (max-width: 768px)`, `@media (max-width: 480px)`).
- Prefer **Flexbox** and **CSS Grid** for structural layouts to allow easy reflowing of elements.
- Avoid absolute unit widths (`px`). Instead, use %, `vw`, `vh`, `em`, and `rem`.

## 6. Testing & Acceptance Criteria
- **DevTools Testing:** verified across the following simulated device sizes in Chrome/Firefox DevTools:
  - Mobile Small (320px)
  - Mobile Large (425px)
  - Tablet (768px)
- **Real Device Testing:** Test physical interaction on at least one iOS (Safari) and one Android (Chrome) device.
- **Success Metrics:**
  - 100% of functionality is usable on a mobile device.
  - No horizontal scrollbars are present on vertical-centric pages (e.g., Recipe Details).
  - Automated layout checks (if any UI tests exist) pass on mobile viewport configurations.

## 7. Next Steps & Timeline
1. Update global base templates (`base.html`, `navbar`).
2. Optimize Recipe List and Detail sheets.
3. Overhaul the Calendar View for mobile.
4. Final QA round and deployment.
