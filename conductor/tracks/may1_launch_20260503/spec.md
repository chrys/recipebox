# Specification: May 1 Launch Features (Clerk, Walkthrough, SEO)

## 1. Overview
This track encompasses a suite of enhancements geared towards user onboarding, SEO/accessibility, and legal compliance. Key features include integrating Clerk.com for authentication, an interactive new-user walkthrough, recipe schema markup, a contact page, and various tracking/sharing additions.

## 2. Functional Requirements

### 2.1 Authentication (Clerk.com)
*   **Sign Up/Login Pages:** Replace existing Django authentication views with Clerk.com drop-in components.
*   **Integration:** Full SDK integration into the Django backend to manage sessions and user synchronization.

### 2.2 SEO & Accessibility
*   **Recipe Schema:** Verify and ensure every recipe page outputs valid JSON-LD `Recipe` schema markup.
*   **Sitemap & Robots:** Automatically generate `sitemap.xml` containing all public recipes and static pages, and serve a `robots.txt`.
*   **Image Alt Text:** Modify image upload logic to automatically generate basic `alt` text using the associated Recipe Title.

### 2.3 User Experience
*   **Print Functionality:** Add a "Print Recipe" button to recipe detail pages that triggers a print-optimized stylesheet.
*   **First-Time Walkthrough:** Implement an interactive tooltip-based guided tour for new users covering:
    *   Adding new recipes.
    *   Searching for recipes.
    *   Scheduling recipes in the calendar.
    *   Populating the shopping list from scheduled recipes.
*   **Social Sharing:** Integrate `django-social-share` to add share buttons (Twitter, Facebook, WhatsApp, Pinterest) to recipe pages.

### 2.4 Static Pages & Tracking
*   **About Page:** Create a simple static page describing the project.
*   **Contact Form:** Create a contact page with a form. Submissions will be sent directly to an admin email address.
*   **Legal Pages:** Create static pages for Privacy Policy and Terms of Service using standard UK templates. Include a simple UK-compliant cookie consent banner.
*   **Analytics:** Embed the provided Google Analytics tag (`G-XBJMD3B73H`) globally.

## 3. Acceptance Criteria
*   Users can successfully register and log in via Clerk.
*   New users see the tooltip walkthrough; returning users do not.
*   Recipe pages pass Google's Rich Results Test for Schema markup.
*   `sitemap.xml` and `robots.txt` are accessible and correctly formatted.
*   Uploaded recipe images automatically receive the recipe title as alt text.
*   Contact form submissions are successfully delivered via email.
*   Social sharing buttons correctly link to respective platforms with the recipe URL.
*   Cookie consent banner appears and functions correctly.

## 4. Out of Scope
*   Migration of existing Django users to Clerk (assuming this is a new launch or handled separately).
*   Custom legal text drafting (using standard UK templates).