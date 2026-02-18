# 🍳 RecipeBox — MVP Task Breakdown

> **Sprint:** Feb-1 (February 2026)  
> **PRD:** [feb1-specs-PRD.md](file:///Users/chrys/Projects/recipes/Design/Feb-26/feb1-specs-PRD.md)  
> **Notes:** No git commits (user manages). Schema.org JSON-LD on all recipe pages.

---

## Phase 1: Project Setup

- [x] **1.1 Create `requirements.txt`**
  - Django 5.x
  - Pillow (image handling)
  - python-dotenv (env vars)
  - psycopg2-binary (PostgreSQL driver for production)

- [x] **1.2 Install dependencies**
  - Activate `.venv` and `pip install -r requirements.txt`

- [x] **1.3 Scaffold Django project**
  - Run `django-admin startproject recipebox .` in project root
  - Create split settings: `recipebox/settings/base.py`, `local.py`, `production.py`
  - Configure `base.py`: installed apps, templates, static/media, auth redirects
  - `local.py`: SQLite database
  - `production.py`: PostgreSQL from env vars
  - Create `.env` with `SECRET_KEY`, `DEBUG=True`, `DJANGO_SETTINGS_MODULE=recipebox.settings.local`

- [x] **1.4 Create Django apps**
  - `python manage.py startapp recipes`
  - `python manage.py startapp calendar_app`
  - `python manage.py startapp accounts`
  - Register all three in `INSTALLED_APPS`

- [x] **1.5 Set up oat-ui static files**
  - Copy `oat.min.css` and `oat.min.js` from `oat-ui/` into `static/oat/`
  - Create `static/css/theme.css` with RecipeBox warm amber colour palette
  - Create `static/js/app.js` (placeholder for ingredient form JS, calendar interactions)

- [x] **1.6 Create base template**
  - `templates/base.html` — oat-ui sidebar layout shell with topnav
  - Include oat CSS/JS + theme.css + app.js via `{% static %}`
  - Sidebar nav: Recipes link, Calendar link
  - Topnav: "RecipeBox" branding, user dropdown (logout)
  - Dark mode toggle button (localStorage preference)
  - `{% block content %}` for page content
  - `templates/base_auth.html` — minimal layout for login/signup (no sidebar)

- [x] **1.7 Run initial migration and verify server starts**
  - `python manage.py migrate`
  - `python manage.py runserver` → verify blank app loads with oat-ui styled shell

---

## Phase 2: Authentication

- [x] **2.1 Accounts — URLs and views**
  - `accounts/urls.py`: login, logout, signup routes
  - `accounts/views.py`: `SignupView` using Django's `UserCreationForm`
  - Wire into `recipebox/urls.py` under `/accounts/`

- [x] **2.2 Auth templates**
  - `accounts/templates/accounts/login.html` — oat-ui form, extends `base_auth.html`
  - `accounts/templates/accounts/signup.html` — oat-ui form, extends `base_auth.html`

- [x] **2.3 Auth settings**
  - `LOGIN_URL`, `LOGIN_REDIRECT_URL = '/recipes/'`, `LOGOUT_REDIRECT_URL = '/accounts/login/'`

- [x] **2.4 Verify auth flow**
  - Sign up → auto login → redirect to `/recipes/`
  - Login / logout cycle works
  - Unauthenticated access to `/recipes/` redirects to login

---

## Phase 3: Recipe Models & Admin

- [x] **3.1 Recipe model**
  - `recipes/models.py`: `Recipe` model with all fields from PRD
  - Fields: user (FK), title, description, instructions, prep_time, cook_time, servings, category (choices), image, created_at, updated_at
  - `__str__`, `get_absolute_url`, `total_time` property

- [x] **3.2 RecipeIngredient model**
  - `recipes/models.py`: `RecipeIngredient` with recipe (FK cascade), name, quantity, order
  - `Meta: ordering = ['order']`

- [x] **3.3 Register in Django admin**
  - `recipes/admin.py`: `RecipeAdmin` with `RecipeIngredientInline` (TabularInline)
  - Allows quick testing of CRUD via admin

- [x] **3.4 Run migrations**
  - `python manage.py makemigrations recipes`
  - `python manage.py migrate`
  - Create superuser for admin access

---

## Phase 4: Recipe CRUD Views & Templates

- [x] **4.1 Recipe forms**
  - `recipes/forms.py`: `RecipeForm` (ModelForm for Recipe)
  - `RecipeIngredientFormSet` — Django inline formset for RecipeIngredient
  - Form validation and error handling

- [x] **4.2 Recipe list view**
  - `recipes/views.py`: `RecipeListView` (ListView, `@login_required`)
  - Filter by current user, search by title/ingredient, filter by category
  - `recipes/urls.py`: `/recipes/` route
  - Template: `recipe_list.html` — responsive card grid using oat-ui Grid + Card
  - Empty state alert when no recipes

- [x] **4.3 Recipe create view**
  - `RecipeCreateView` — form + ingredient formset
  - Template: `recipe_form.html` — oat-ui form fields, dynamic ingredient rows
  - `static/js/app.js`: JavaScript for add/remove ingredient rows in formset
  - Redirect to detail on success

- [x] **4.4 Recipe detail view**
  - `RecipeDetailView` (DetailView, `@login_required`, owner check)
  - Template: `recipe_detail.html`
  - Hero image, title, category badge, time, servings
  - `<ot-tabs>` with Ingredients and Instructions tabs
  - Action buttons: Edit, Delete (with `<dialog>` confirmation), Add to Calendar
  - **Schema.org JSON-LD** `<script type="application/ld+json">` block with Recipe schema

- [x] **4.5 Schema.org JSON-LD integration**
  - Create `recipes/templatetags/recipe_schema.py` — custom template tag
  - Generates JSON-LD output following [schema.org/Recipe](https://schema.org/Recipe) spec
  - Fields mapped: `name`, `description`, `recipeIngredient`, `recipeInstructions`, `prepTime` (ISO 8601 duration), `cookTime`, `totalTime`, `recipeYield`, `recipeCategory`, `image`, `datePublished`
  - Include in `recipe_detail.html` via `{% recipe_json_ld recipe %}`
  - Also include in `recipe_list.html` as an `ItemList` of recipes

- [x] **4.6 Recipe edit view**
  - `RecipeUpdateView` — same form as create, pre-populated
  - Template: reuse `recipe_form.html` (with context flag for edit vs create title)
  - Owner permission check
  - Redirect to detail on success

- [x] **4.7 Recipe delete view**
  - `RecipeDeleteView` — POST-only, owner check
  - Uses `<dialog>` confirmation on the detail/edit template (client-side)
  - Redirect to list on success

- [x] **4.8 Wire recipe URLs**
  - `recipes/urls.py`: all CRUD routes
  - Include in `recipebox/urls.py` under `/recipes/`
  - Root `/` redirects to `/recipes/`

---

## Phase 5: Calendar

- [x] **5.1 CalendarEntry model**
  - `calendar_app/models.py`: `CalendarEntry` with user (FK), recipe (FK cascade), date, meal_type (choices), created_at
  - `Meta: unique_together = ['user', 'recipe', 'date', 'meal_type']`

- [x] **5.2 Run calendar migrations**
  - `python manage.py makemigrations calendar_app`
  - `python manage.py migrate`

- [x] **5.3 Calendar form**
  - `calendar_app/forms.py`: `CalendarEntryForm` — recipe (filtered to user's recipes), date, meal_type

- [x] **5.4 Calendar view**
  - `calendar_app/views.py`: `CalendarView` (`@login_required`)
  - Generate monthly grid using Python's `calendar` module
  - Query `CalendarEntry` objects for the displayed month
  - Map entries to day cells
  - Month navigation (prev/next via query params `?year=&month=`)
  - Template: `calendar_app/calendar.html` — HTML `<table>`, day cells with recipe badges
  - "+" button per day cell → opens `<dialog>` to add recipe
  - Today highlighting

- [x] **5.5 Add to calendar view**
  - `CalendarAddView` — POST-only, `@login_required`
  - Accepts recipe_id, date, meal_type
  - Validates unique constraint
  - Redirect back to calendar with success toast
  - Also accessible from recipe detail page dialog

- [x] **5.6 Remove from calendar view**
  - `CalendarDeleteView` — POST-only, `@login_required`, owner check
  - Redirect back to calendar with toast

- [x] **5.7 Wire calendar URLs**
  - `calendar_app/urls.py`: calendar view, add, delete routes
  - Include in `recipebox/urls.py` under `/calendar/`

---

## Phase 6: Polish & Integration

- [x] **6.1 Toast notifications**
  - Add Django messages framework integration
  - In `base.html`, render `{% for message in messages %}` as `ot.toast()` calls
  - Success/error/warning variants mapped to oat-ui toast variants

- [x] **6.2 Form validation UX**
  - Style Django form errors with oat-ui `data-field="error"` pattern
  - Create a reusable `_form_field.html` include for consistent error display

- [x] **6.3 Responsive recipe grid**
  - Verify 3-column → 2-column → 1-column layout on recipe list
  - Test sidebar collapse on mobile

- [x] **6.4 Empty states**
  - Recipe list empty: alert with "Create your first recipe" CTA
  - Calendar month empty: subtle message in the calendar

- [x] **6.5 Image placeholder**
  - Default placeholder image when recipe has no uploaded photo
  - Generate a simple SVG placeholder or use a CSS-based placeholder

- [x] **6.6 Media file serving (dev)**
  - Configure `urls.py` to serve `MEDIA_URL` in development (`DEBUG=True`)

---

## Phase 7: Verification

- [x] **7.1 Manual testing checklist**
  - Sign up new user
  - Create recipe with image, ingredients, all fields
  - View recipe detail — verify tabs, badges, image, JSON-LD in page source
  - Edit recipe — change fields, add/remove ingredients
  - Delete recipe — dialog confirmation, redirect
  - Search and filter on recipe list
  - Calendar — navigate months, add recipe to date, view badges
  - Remove recipe from calendar
  - Logout / login cycle
  - Mobile responsive checks (resize browser)
  - Dark mode toggle

- [x] **7.2 Schema.org validation**
  - Copy JSON-LD from recipe detail page source
  - Validate at [Google Rich Results Test](https://search.google.com/test/rich-results)
  - Verify all fields render correctly

- [x] **7.3 Final cleanup**
  - Remove any debug prints
  - Ensure `DEBUG=True` only in `local.py`
  - Verify `.env` is in `.gitignore`
  - Confirm `db.sqlite3` is in `.gitignore`
