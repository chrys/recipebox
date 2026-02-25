# 🍳 RecipeBox — Product Requirements Document (MVP)

> **Version:** 1.0  
> **Date:** February 16, 2026  
> **Status:** Draft  

---

## 1. Product Overview

**RecipeBox** is a personal recipe management web application where users can create, organise, and plan their meals using a built-in calendar. The MVP focuses on delivering a clean, fast, and simple experience for a single authenticated user to manage their recipe collection and weekly/monthly meal plans.

### 1.1 Goals
- Allow users to **Create, Read, Update, Delete (CRUD)** recipes
- Provide a **calendar view** where users can assign and remove recipes on specific dates
- Deliver a **lightweight, fast UI** using the oat-ui semantic component library
- Run on **Django** with SQLite locally and PostgreSQL in production

### 1.2 Target User
Home cooks who want a simple, private tool to store recipes and plan meals — without the bloat of social features, ads, or complexity.

---

## 2. Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| **Backend** | Django 5.x | Python web framework |
| **Database (local)** | SQLite | Zero-config for development |
| **Database (prod)** | PostgreSQL | Configured via environment variable |
| **Frontend UI** | [oat-ui](https://oat.ink) | ~8KB semantic HTML/CSS/JS library, no build step |
| **Templates** | Django Templates | Server-side rendered with oat-ui components |
| **Auth** | Django built-in auth | `django.contrib.auth` |
| **Media/Images** | Django file storage | Recipe photos stored via `MEDIA_ROOT` |

### 2.1 oat-ui Analysis

oat-ui (`@knadh/oat`) is an ultra-lightweight, zero-dependency UI library that styles semantic HTML elements directly. It is an excellent fit for Django template-based rendering.

**Key characteristics:**
- **~8KB total** (CSS + JS combined) — no build tools required
- **Semantic HTML** — styles `<button>`, `<table>`, `<form>`, `<dialog>` etc. automatically without classes
- **WebComponents** — `<ot-tabs>`, `<ot-dropdown>` for interactive widgets
- **CSS variable theming** — full customisation via `--primary`, `--background`, etc.
- **Dark mode** — via `data-theme="dark"` on `<body>`

**Available components we will use:**

| Component | Usage in RecipeBox |
|-----------|--------------------|
| **Sidebar layout** (`data-sidebar-layout`) | App shell with navigation |
| **Topnav** (`data-topnav`) | Header bar with app name and user menu |
| **Cards** (`.card` on `<article>`) | Recipe cards in list/grid view |
| **Forms** (`data-field`, `<label>`) | Recipe create/edit forms |
| **Dialog** (`<dialog>` + `commandfor`) | Delete confirmation, quick-add recipe to calendar |
| **Tabs** (`<ot-tabs>`) | Recipe detail view (Ingredients / Instructions / Notes) |
| **Table** (`<table>`) | Admin-style recipe list view |
| **Grid** (`.container`, `.row`, `.col-*`) | Responsive recipe card layout |
| **Dropdown** (`<ot-dropdown>`) | User menu, recipe action menus |
| **Toast** (`ot.toast()`) | Success/error notifications |
| **Alert** (`role="alert"`) | Form validation errors, empty states |
| **Badge** (`.badge`) | Recipe tags/categories, meal type labels |
| **Spinner** | Loading states |
| **Skeleton** | Page-load placeholders |
| **Button** variants | Primary, outline, danger, ghost actions |
| **Accordion** | FAQ or collapsible recipe sections |

**Integration with Django:**
- Include `oat.min.css` and `oat.min.js` as static files in Django's `staticfiles`
- No npm/build pipeline needed — just copy the dist files
- Custom theme CSS loaded after oat to set the RecipeBox colour palette

---

## 3. Data Model

### 3.1 Entity Relationship

```
User (Django Auth)
 ├── Recipe (1:N)
 │    ├── RecipeIngredient (1:N)
 │    └── RecipeImage (1:N, optional)
 └── CalendarEntry (1:N)
      └── Recipe (M:1)
```

### 3.2 Models

#### `Recipe`
| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField | PK |
| `user` | ForeignKey(User) | Owner |
| `title` | CharField(200) | Required |
| `description` | TextField | Short summary, optional |
| `instructions` | TextField | Step-by-step cooking instructions |
| `prep_time` | PositiveIntegerField | In minutes, optional |
| `cook_time` | PositiveIntegerField | In minutes, optional |
| `servings` | PositiveIntegerField | Number of servings, optional |
| `category` | CharField + choices | Breakfast / Lunch / Dinner / Snack / Dessert |
| `image` | ImageField | Main recipe photo, optional |
| `created_at` | DateTimeField | Auto |
| `updated_at` | DateTimeField | Auto |

#### `RecipeIngredient`
| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField | PK |
| `recipe` | ForeignKey(Recipe) | Cascade delete |
| `name` | CharField(200) | e.g. "Flour" |
| `quantity` | CharField(50) | e.g. "2 cups", free-text to allow "pinch", "to taste" |
| `order` | PositiveIntegerField | Display order |

#### `CalendarEntry`
| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField | PK |
| `user` | ForeignKey(User) | Owner |
| `recipe` | ForeignKey(Recipe) | Cascade delete |
| `date` | DateField | Which day |
| `meal_type` | CharField + choices | Breakfast / Lunch / Dinner / Snack |
| `created_at` | DateTimeField | Auto |

**Constraint:** Unique together on `(user, recipe, date, meal_type)` — prevent duplicate assignments.

---

## 4. Feature Specifications

### 4.1 Authentication

| Feature | Details |
|---------|---------|
| **Sign up** | Email + password registration via Django auth |
| **Log in / Log out** | Standard Django session-based auth |
| **Protected routes** | All app pages require `@login_required` |

**UI:** Simple full-page forms using oat-ui form styling. No sidebar on auth pages.

---

### 4.2 Recipe CRUD

#### 4.2.1 Recipe List (Home Page)

**Route:** `/recipes/`

**Layout:** Sidebar + main content area using `data-sidebar-layout`

**Features:**
- Display all user's recipes as **cards** in a responsive grid (`.col-4` on desktop, `.col-6` tablet, full-width mobile)
- Each card shows: image thumbnail (or placeholder), title, category badge, prep+cook time
- **Search bar** at the top (filter by title, ingredient)
- **Category filter** dropdown
- **"+ New Recipe"** primary button in the header
- **Empty state:** Alert with call-to-action when no recipes exist

**oat-ui components:** Grid, Card, Badge, Button, Alert, Dropdown, Spinner

#### 4.2.2 Recipe Create

**Route:** `/recipes/new/`

**Features:**
- Form with fields: title, description, category (select), prep time, cook time, servings, image upload
- **Dynamic ingredients** section: add/remove ingredient rows (name + quantity) via JavaScript
- **Instructions** textarea (plain text, one step per line)
- Save button → redirect to recipe detail
- Cancel button → back to list
- Client-side + server-side validation with `data-field="error"` styling

**oat-ui components:** Form fields, Button, Alert (validation)

#### 4.2.3 Recipe Detail

**Route:** `/recipes/<id>/`

**Features:**
- Hero image (or placeholder)
- Title, category badge, time info, servings
- **Tabbed content** using `<ot-tabs>`:
  - **Ingredients** tab — ordered list of ingredients
  - **Instructions** tab — numbered steps
- Action buttons: **Edit** (outline), **Delete** (danger, opens confirmation dialog), **Add to Calendar** (opens dialog with date picker + meal type select)
- Toast notification on actions (e.g. "Recipe deleted", "Added to calendar")

**oat-ui components:** Tabs, Badge, Button, Dialog, Toast

#### 4.2.4 Recipe Edit

**Route:** `/recipes/<id>/edit/`

**Features:**
- Same form as Create, pre-populated with existing data
- Can update/remove/reorder ingredients
- Save → redirect to detail, Toast "Recipe updated"
- Delete button available here too

#### 4.2.5 Recipe Delete

**Trigger:** Button on detail or edit page

**Flow:**
1. Click "Delete" button
2. oat-ui `<dialog>` confirmation appears: "Are you sure you want to delete **{title}**? This cannot be undone."
3. Confirm → POST to delete endpoint → redirect to list with Toast "Recipe deleted"
4. Cancel → close dialog

---

### 4.3 Meal Calendar

#### 4.3.1 Calendar View

**Route:** `/calendar/`

**Layout:** Main content area (same sidebar shell)

**Features:**
- **Monthly calendar grid** rendered server-side as an HTML `<table>`
- Each day cell shows assigned recipes as small **badges** (colour-coded by meal_type)
- Click on a recipe badge → navigate to recipe detail
- **"+"** button on each day cell → opens dialog to add a recipe
- **Month navigation** — Previous / Next month buttons, "Today" link
- Current day highlighted

**oat-ui components:** Table, Badge, Button, Dialog, Dropdown

#### 4.3.2 Add Recipe to Calendar

**Trigger:** "+" button on a calendar day, or "Add to Calendar" on recipe detail

**Flow (from calendar):**
1. Click "+" on a day → opens `<dialog>`
2. Dialog contains:
   - The selected date (pre-filled, read-only)
   - Recipe select dropdown (search/filter the user's recipes)
   - Meal type radio buttons (Breakfast / Lunch / Dinner / Snack)
3. Submit → POST → page refreshes with Toast "Recipe added to {date}"

**Flow (from recipe detail):**
1. Click "Add to Calendar" → opens `<dialog>`
2. Dialog contains:
   - Recipe name (pre-filled, read-only)
   - Date picker input
   - Meal type radio buttons
3. Submit → POST → Toast "Added to {date}"

#### 4.3.3 Remove Recipe from Calendar

**Trigger:** Click on a recipe badge in the calendar

**Flow:**
1. Click recipe badge → dropdown with "View Recipe" and "Remove from Calendar"
2. "Remove" → confirmation dialog → POST delete → page refresh with Toast

---

## 5. Page Map & URL Structure

| URL | View | Description |
|-----|------|-------------|
| `/` | Redirect | → `/recipes/` |
| `/accounts/signup/` | SignupView | Registration |
| `/accounts/login/` | LoginView | Login |
| `/accounts/logout/` | LogoutView | Logout |
| `/recipes/` | RecipeListView | All recipes (home) |
| `/recipes/new/` | RecipeCreateView | Create recipe form |
| `/recipes/<id>/` | RecipeDetailView | Recipe detail with tabs |
| `/recipes/<id>/edit/` | RecipeUpdateView | Edit recipe form |
| `/recipes/<id>/delete/` | RecipeDeleteView | POST-only delete |
| `/calendar/` | CalendarView | Monthly calendar |
| `/calendar/add/` | CalendarAddView | POST-only add entry |
| `/calendar/<id>/delete/` | CalendarDeleteView | POST-only remove entry |

---

## 6. Django App Structure

```
recipebox/                      # Project root
├── manage.py
├── recipebox/                  # Django project settings
│   ├── settings/
│   │   ├── base.py             # Shared settings
│   │   ├── local.py            # SQLite config
│   │   └── production.py       # PostgreSQL config
│   ├── urls.py
│   └── wsgi.py
├── recipes/                    # Recipes app
│   ├── models.py               # Recipe, RecipeIngredient
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── recipes/
│           ├── recipe_list.html
│           ├── recipe_detail.html
│           ├── recipe_form.html
│           └── recipe_confirm_delete.html
├── calendar_app/               # Calendar app (avoid name clash with stdlib)
│   ├── models.py               # CalendarEntry
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
│       └── calendar_app/
│           └── calendar.html
├── accounts/                   # Auth app
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
│       └── accounts/
│           ├── login.html
│           └── signup.html
├── templates/                  # Global templates
│   └── base.html               # oat-ui shell (sidebar + topnav)
├── static/
│   ├── oat/                    # oat-ui dist files
│   │   ├── oat.min.css
│   │   └── oat.min.js
│   ├── css/
│   │   └── theme.css           # RecipeBox custom theme overrides
│   └── js/
│       └── app.js              # Ingredients form JS, calendar interactions
├── media/                      # User-uploaded recipe images
├── requirements.txt
└── .env                        # DB config, SECRET_KEY, DEBUG
```

---

## 7. UI / UX Design Decisions

### 7.1 Layout
- **Sidebar** navigation with links: 🏠 Recipes, 📅 Calendar
- **Topnav** with app name "RecipeBox" and user dropdown (Profile, Logout)
- On mobile: sidebar collapses to hamburger menu via `data-sidebar-toggle`

### 7.2 Theme
Custom warm food-inspired colour palette via oat-ui CSS variables:

```css
:root {
  --primary: #d97706;           /* Warm amber */
  --primary-foreground: #fff;
  --secondary: #fef3c7;         /* Light cream */
  --secondary-foreground: #92400e;
  --accent: #f59e0b;            /* Gold accent */
  --background: #fffbeb;        /* Warm white */
  --foreground: #1c1917;
  --card: #ffffff;
  --border: #e5e7eb;
  --muted: #f5f5f4;
  --muted-foreground: #78716c;
  --danger: #dc2626;
  --success: #16a34a;
  --warning: #f59e0b;
}
```

### 7.3 Dark Mode
- Toggle via button in topnav that sets `data-theme="dark"` on `<body>`
- User preference saved in `localStorage`

### 7.4 Responsive Behaviour
- Recipe grid: 3 columns → 2 → 1 as viewport narrows
- Calendar: horizontal scroll on mobile for the table
- Sidebar: slides in/out on mobile

---

## 8. MVP Suggestions & Recommendations

### ✅ What to include in MVP

1. **Django's built-in auth** — No need for social login, Clerk, or third-party auth for an MVP. Keep it simple.
2. **Server-side rendering** — No need for a separate JS frontend or API. Django templates + oat-ui give a fast, clean experience with zero complexity.
3. **Free-text ingredient quantities** — Don't over-engineer with separate quantity/unit fields. "2 cups" or "a pinch" as free text is far more practical.
4. **Static file hosting for oat-ui** — Copy the `oat.min.css` and `oat.min.js` into Django's `static/` folder. No npm, no build pipeline.
5. **Simple monthly calendar** — Server-rendered HTML table. No need for a heavy JS calendar library.
6. **Image upload** — One image per recipe via Django's `ImageField`. Use Pillow for thumbnail generation.
7. **Search** — Simple `icontains` filter on title + ingredient names. No need for Elasticsearch.

### ⏳ What to defer to post-MVP

| Feature | Why defer |
|---------|-----------|
| Recipe tags/labels | Categories are sufficient for MVP |
| Shopping list generation | Nice-to-have, not core |
| Recipe import (URL scraping) | Complex, requires parsing various sites |
| Sharing/public profiles | MVP is single-user/private |
| Nutritional information | Requires external API integration |
| Drag-and-drop calendar | Significant JS work; badge + dialog is simpler |
| Recipe scaling (adjust servings) | Math logic for fraction conversion |
| Print-friendly view | CSS `@media print` — quick win for v1.1 |
| Weekly view for calendar | Monthly is sufficient for MVP |
| REST API | Not needed if server-rendered |

---

## 9. Database Configuration

### Local (SQLite)
```python
# settings/local.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Production (PostgreSQL)
```python
# settings/production.py
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'recipebox'),
        'USER': os.environ.get('DB_USER', 'recipebox'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

**Switching environments** via `DJANGO_SETTINGS_MODULE`:
```bash
# Local
export DJANGO_SETTINGS_MODULE=recipebox.settings.local

# Production
export DJANGO_SETTINGS_MODULE=recipebox.settings.production
```

---

## 10. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| **Page load** | < 1s (oat-ui is ~8KB, SSR templates are fast) |
| **Mobile responsive** | Works on all screen sizes via oat-ui grid + sidebar |
| **Accessibility** | oat-ui uses semantic HTML + ARIA roles by default |
| **Browser support** | Modern browsers (Chrome, Firefox, Safari, Edge) |
| **Security** | Django CSRF protection, `@login_required`, input sanitisation |
