# Sweetiverse

# Table of Contents

-   [User Experience](#user-experience)
    -   [User Stories](#user-stories)
    -   [Site Goals](#site-goals)
    -   [Scope](#scope)
-   [Design](#design)
    -   [Colour Scheme](#colour-scheme)
    -   [Database Schema](#Database-Schema)
    -   [Fonts](#Fonts)
    -   [Wireframes](#Wireframes)
    -   [Agile Methodology](#Agile-Methodology)
         -   [Overview](#overview)
         -   [EPICS(Milestones)](#epicsmilestones)
         -   [User Stories issues](#user-stories-issues)
         -   [MoSCoW prioritization](#moscow-prioritization)
         -   [GitHub Projects](#github-projects)
-   [Features](#features)
-   [Future Features](#future-features)
-   [Marketing](#marketing)
-   [Search Engine Optimization SEO](#search-engine-optimization-seo)
-   [Testing](#testing)
-   [Bugs](#Bugs)
-   [Technologies And Languages](#technologies-and-languages)
    -   [Languages Used](#languages-used)
    -   [Python Modules](#python-modules)
    -   [Technologies and programs](#technologies-and-programs)
-   [Deployment](#deployment)
    -   [Before Deployment](#before-deployment)
    -   [Deployment on Heroku](#deployment-on-heroku)
    -   [Creating A Fork](#creating-a-fork)
    -   [Cloning Repository](#cloning-repository)
-   [Credits](#credits)
    -   [Media](#media)
    -   [Code](#code)
    -   [Acknowledgements](#acknowledgements)
    -   [Comments](#comments)

## User Experience

### User Stories

#### Developer Stories
- As a developer, I can set up a new Django project so that I can establish the project structure.
- As a developer, I can connect the database and media storage so that user data and images are stored successfully.
- As a developer, I can deploy the application early so that I can verify everything works and continue testing during development.

#### General User Stories
- As a user, I can visit the homepage so I understand the purpose of Sweetiverse.
- As a user, I can navigate the website efficiently to access different sections like products, help, or cart.
- As a user, I want to be able to view all available sweets so that I can browse and discover treats to purchase.
- As a user, I want to view detailed information about a single sweet so I can make informed decisions.
- As a user, I want to filter sweets by country or category so I can find exactly what I’m interested in.
- As a user, I want to search for sweets by keywords so that I can quickly find specific items.
- As a user, I want to sort the sweet list by name or price so I can easily compare options.

#### Authenticated User Stories
- As a user, I want to register an account so I can access full functionality.
- As a user, I want to log in to my account so I can personalize my experience.
- As a user, I want to reset my password if I forget it so I can regain access.
- As a user, I want to update my profile information so I can keep my account current.
- As an authenticated user, I want to leave reviews for sweets so I can share feedback.
- As an authenticated user, I want to edit or delete my reviews to keep them relevant.
- As an authenticated user, I want to add sweets to my wishlist so I can save them for later.

#### Shopping Cart & Checkout
- As a user, I want to add products to my cart so I can review them before purchase.
- As a user, I want to remove items from my cart so I can adjust my order.
- As a user, I want to adjust the quantity of items in my cart for accurate purchasing.
- As a user, I want to apply discount codes to get deals and savings.
- As a user, I want to securely pay for items using Stripe so I can complete purchases confidently.
- As a user, I want to complete checkout easily so I can buy sweets without friction.

#### Admin Stories
- As an admin, I want to view an admin dashboard to monitor orders and activity.
- As an admin, I want to add, update, or delete sweets so I can manage the inventory.
- As an admin, I want to adjust stock levels to maintain availability.

#### Extra User Features
- As a user, I want to submit a testimonial about my experience to share feedback.
- As a user, I want to read other users’ testimonials to build trust.
- As a user, I want to sign up for a newsletter so I can stay updated with offers.

#### SEO / Business Goals
- As the site owner, I want the site to be SEO optimized so Sweetiverse ranks higher and attracts more users.

---

### Site Goals

- Provide users with a global marketplace for international sweets.
- Allow users to browse, search, and filter sweets by country or type.
- Enable customers to register accounts, manage orders, and maintain wishlists.
- Support user-generated reviews and testimonials on sweets.
- Streamline and secure the checkout process.

---

### Scope

The project aims to deliver a responsive and user-friendly sweets e-commerce platform. Core features include:

- User registration, login, and password reset  
- Sweet browsing, searching, filtering, and sorting  
- Product detail pages  
- Shopping cart (add, remove, update items)  
- Wishlist functionality  
- Reviews and testimonials  
- Secure checkout using Stripe  
- Newsletter signup  
- Admin management for inventory and orders

## Design

### Color Scheme

### Database Schema
![database schema](./assets/readme-images/erd.png)

#### User
Django's built-in User model

#### UserProfile
- id (Primary Key)
- user (One-to-One Field to User)
- default_phone_number (CharField)
- default_street_address1 (CharField)
- default_street_address2 (CharField)
- default_town_or_city (CharField)
- default_county (CharField)
- default_postcode (CharField)
- default_country (CountryField)

#### Sweet
Represents an individual sweet product
- id (UUID)
- name (CharField)
- description (TextField)
- image (ImageField)
- ingredients (TextField)
- flavor (CharField)
- country_of_origin (CountryField)
- type (ForeignKey to Type)
- stock_amount (IntegerField)
- in_stock (BooleanField)
- on_sale (BooleanField)
- price (DecimalField)
- discount (IntegerField)
- sale_price (DecimalField)
- created (DateTimeField)

#### Type
Represents a sweet type (e.g. chocolate, gummy, hard candy)
- id (Primary Key)
- name (CharField)
- friendly_name (CharField)
- category (ForeignKey to Category)

#### Category
Categorization of types
- name (CharField)

#### SweetReview
User-generated review for a sweet
- user (ForeignKey to UserProfile)
- sweet (ForeignKey to Sweet)
- rating (IntegerField)
- review (TextField)
- created (DateTimeField)

#### WishList
A user's saved list of favorite sweets
- user (ForeignKey to UserProfile)
- sweet (ForeignKey to Sweet)
- created (DateTimeField)

#### Order
Tracks all order details
- id (Primary Key)
- order_number (CharField)
- user_profile (ForeignKey to UserProfile)
- full_name (CharField)
- email (EmailField)
- phone_number (CharField)
- country (CountryField)
- postcode (CharField)
- town_or_city (CharField)
- street_address1 (CharField)
- street_address2 (CharField)
- county (CharField)
- date (DateTimeField)
- delivery_cost (DecimalField)
- discount (DecimalField)
- order_total (DecimalField)
- grand_total (DecimalField)
- original_cart (TextField)
- stripe_pid (CharField)

#### OrderLineItem
Individual sweet items in an order
- order (ForeignKey to Order)
- sweet (ForeignKey to Sweet)
- quantity (IntegerField)
- lineitem_total (DecimalField)

#### Order Status
Tracks the current status of an order
- order (One-to-One Field to Order)
- status (CharField)

#### Discount Code
Promotional codes for users to apply at checkout
- code (CharField)
- discount (IntegerField)
- active (BooleanField)

#### PickNMix
A user-selected bundle of random sweets
- user (ForeignKey to UserProfile)
- quantity (IntegerField)
- created (DateTimeField)
- sweets (ManyToManyField to Sweet)
- total_price (DecimalField)

#### SubscriptionBox
Monthly sweet box sent to a user
- user (ForeignKey to UserProfile)
- start_date (DateTimeField)
- active (BooleanField)
- sweets (ManyToManyField to Sweet)
- country_selection (Optional CharField or JSONField)

# Search Engine Optimization SEO

## SEO Keyword Research Process

### Business Description
SweetiVERSE is an e-commerce application offering a customizable international pick-n-mix sweets subscription. Users can create a personalized sweets box with candy from various countries and themes, with future expansions planned for additional regions and dietary options.

---

### 1. Brainstorm General Topics

These are core subject areas relevant to SweetiVERSE:

- Pick n mix
- International candy
- Subscription boxes
- Sweet treats
- Global sweets
- Candy delivery
- Themed sweets
- Allergen-safe sweets

---

### 2. Brain Dump of Keyword Ideas

#### Pick n mix:
- pick n mix
- pick and mix sweets
- online pick n mix
- custom pick n mix box

#### International candy:
- candy from around the world
- international sweets
- sweets from Europe
- Japanese candy box
- Swedish sweets online

#### Subscription:
- candy subscription
- monthly sweets box
- pick n mix subscription
- sweet subscription UK

#### Themed treats:
- themed candy boxes
- holiday candy box
- best sweets for gifts

#### Allergy-friendly:
- peanut-free sweets
- sugar-free candy
- gluten-free pick n mix

---

### 3. Google Research Simulation

Using tools like Google autocomplete, "People Also Ask", and "Related Searches", we simulated search behavior and confirmed interest in the following:

- "Where to buy international candy?"
- "Best candy subscription box"
- "Candy box for kids with allergies"
- "Sweets from Sweden"
- "How to make your own pick n mix?"

These results indicate active search interest in SweetiVERSE’s target features.

---

### 4. Final Keyword List

| Short-Tail Keywords           | Long-Tail Keywords                                       |
|------------------------------|----------------------------------------------------------|
| pick n mix                   | buy international candy online                          |
| candy subscription           | monthly pick and mix sweets box                         |
| international sweets         | pick n mix subscription box UK                          |
| themed candy                 | peanut-free sweets for kids                             |
| global sweets                | Swedish sweets subscription                             |
| sweetiverse                  | create your own pick n mix online                       |
| sweets delivery              | custom sweet box with global candy                      |
| allergen-free candy          | sugar-free candy options for monthly subscription       |

---

### 5. Keyword Strategy

The final keywords were selected based on the following criteria:

- **Relevance** to SweetiVERSE’s products and user needs
- **Balance** of short-tail and long-tail keywords
- **Specificity** to match high-intent user searches
- **Potentially lower competition** due to niche focus

This list will be used to optimize page titles, meta tags, headers, alt text, and on-page content.



## SEO-Friendly Meta Tags

## Semantic HTML

## Keywords in Page Content

## Optimized Image Names and Alt Texts

## Sitemap and Robots.txt

## Meaningful Internal and External Links

## FAQ Page

## Clear, Trustworthy Content
(Terms & Conditions, Privacy Policy, Shipping Info, and Allergen Info) 

## Track Engagement Metrics

### Google Search Console CTR, Bounce Rate, Dwell Time, Pages per session

