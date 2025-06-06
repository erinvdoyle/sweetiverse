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