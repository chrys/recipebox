# Implementation Plan: May 1 Launch Features

## Phase 1: Authentication (Clerk.com)
- [ ] Task: Integrate Clerk Python SDK & Middleware
    - [ ] Create `Tests/unit/accounts/test_clerk_auth.py` and write failing tests for authentication flow.
    - [ ] Install Clerk SDK and configure environment variables.
    - [ ] Set up Clerk authentication middleware in Django backend.
- [ ] Task: Update Frontend Authentication Views
    - [ ] Update `accounts/templates/accounts/login.html` and `signup.html` to use Clerk drop-in components.
    - [ ] Configure Clerk URLs for successful sign-in/sign-up redirects.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Authentication (Clerk.com)' (Protocol in workflow.md)

## Phase 2: SEO, Accessibility & Sharing
- [ ] Task: Recipe Schema Markup
    - [ ] Create `Tests/unit/recipes/test_schema.py` and write failing tests for JSON-LD generation.
    - [ ] Update `recipes/templatetags/recipe_schema.py` to ensure all recipes output valid `Recipe` schema.
    - [ ] Update recipe detail template to include the schema script.
- [ ] Task: Sitemap & Robots.txt
    - [ ] Create `Tests/unit/core/test_sitemap.py` and write failing tests for sitemap and robots.txt generation.
    - [ ] Implement standard Django sitemap framework for recipes and static pages.
    - [ ] Add `robots.txt` view and URL configuration.
- [ ] Task: Image Alt Text Generation
    - [ ] Create `Tests/unit/recipes/test_image_upload.py` and write failing tests for auto-alt text generation.
    - [ ] Update recipe image upload logic to populate alt text from the recipe title.
- [ ] Task: Social Sharing Integration
    - [ ] Install and configure `django-social-share`.
    - [ ] Update recipe detail template with sharing buttons (Twitter, Facebook, WhatsApp, Pinterest).
- [ ] Task: Conductor - User Manual Verification 'Phase 2: SEO, Accessibility & Sharing' (Protocol in workflow.md)

## Phase 3: User Experience (Walkthrough & Print)
- [ ] Task: Print Functionality
    - [ ] Create `Tests/unit/recipes/test_print_view.py` and write tests for print template rendering.
    - [ ] Add print button to recipe detail page.
    - [ ] Create print media queries in `theme.css` to optimize the recipe view for printing.
- [ ] Task: First-Time User Walkthrough
    - [ ] Implement tooltip library (using Vanilla JS/CSS).
    - [ ] Write JS logic in `app.js` to track "first login" state (e.g., using LocalStorage).
    - [ ] Define and implement tooltip steps for adding recipes, searching, scheduling, and shopping lists.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: User Experience (Walkthrough & Print)' (Protocol in workflow.md)

## Phase 4: Static Pages, Forms & Compliance
- [ ] Task: About & Legal Pages
    - [ ] Create `Tests/unit/core/test_static_pages.py` and write tests for static page availability.
    - [ ] Create templates and views for About, Privacy Policy, and Terms of Service pages.
    - [ ] Configure URLs for the new pages.
- [ ] Task: Cookie Consent & Analytics
    - [ ] Add UK-compliant simple cookie consent banner to `base.html`.
    - [ ] Embed Google Analytics tag (`G-XBJMD3B73H`) in `base.html` globally.
- [ ] Task: Contact Form
    - [ ] Create `Tests/unit/core/test_contact_form.py` and write failing tests for form submission and email delivery.
    - [ ] Create Contact form and view logic.
    - [ ] Configure Django email backend for sending submissions to the admin.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Static Pages, Forms & Compliance' (Protocol in workflow.md)