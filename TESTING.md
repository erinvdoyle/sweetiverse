Go back to [README.md](/README.md)

# Testing
- [Code Validation](#code-validation)
    - [HTML](#html)
    - [CSS](#css)
    - [JavaScript](#JavaScript)
    - [Python](#python)
- [Responsiveness](#Responsiveness)
- [Browser Compatibility](#browser-compatibility)
- [Lighthouse](#Lighthouse)
- [Manual Testing](#manual-testing)
- [User Story Testing](#user-story-testing)
- [Stripe](#stripe)

## Code Validation
## HTML Validation Tests

- **HTML Validation**: Used the [W3C HTML Validator](https://validator.w3.org/) and returned the following results:

![HTML Validation](./assets/testing-images/pp5html.png)

These errors were not found in the code and I believe are due to Django tags and extending base.html through the index and all other pages

## CSS Validation Tests

- **CSS Validation**: Used the [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) and returned the following results:

![CSS Validation](./assets/testing-images/cssvalid.png)

## JavaScript
 **JavaScript Validation**: Used the [JShint Validator](https://jigsaw.w3.org/css-validator/) and this is an example of JS hint results from the site JavaScript. No console errors were found during testing and all implementation worked as designed:

![JS Validation](./assets/testing-images/pp5jsvalid.png)

## Python

**Python Validation**: Python files were validated using [CI Python Linter](https://pep8ci.herokuapp.com/) for PEP8 compliance.
To the best of my knowledge, all python logic throughout the project functions error free. I used the flake8 extension to help validate and format code as I worked. Most flagged issues occurred through lines > 79 characters. Most I have fixed, but some remain for the greater good of a working project

## Responsiveness
...
![responsiveness](./assets/readme-images/pp5resp0.png)

Testing of each page was conducted with AMIRESPONSIVE? I downloaded the Ignore X-Frames Headers Chrome Extension, thanks to this helpful article, which allowed me to bypass issues created by the Django tags: https://techsini.com/unable-to-generate-mockup-of-your-website-here-is-the-quick-fix/

<details>
<summary>AMIRESPONSIVE Screenshots (click)</summary>

<img src="assets/testing-images/pp5resp1.png" width="550px"/>
<img src="assets/testing-images/pp5resp2.png" width="550px"/>
<img src="assets/testing-images/pp5resp3.png" width="550px"/>
<img src="assets/testing-images/pp5resp4.png" width="550px"/>
<img src="assets/testing-images/pp5resp5.png" width="550px"/>
<img src="assets/testing-images/pp5resp6.png" width="550px"/>

</details>

SWEETiVERSE has been manually tested on an iPhone 13 Pro and an iPhone 12 for mobile, returning zero issues and passing
For desktop, SWEETiVERSE has been manually tested on a Windows Elitebook


## Browser Compatibility

|Browser|Result|Pass/Fail|Notes|
| --- | --- | --- | ---|
| Google Chrome | All pages load as expected. All features work as expected | PASS | --- |
| Safari | All pages load as expected. All features work as expected | PASS | --- |
| Edge | All pages load as expected. All features work as expected | PASS | ---|

## Lighthouse

- **Lighthouse Scores**: Used [Lighthouse Metrics](https://lighthouse-metrics.com/) to measure scores. SEO and Best Practices hit 100 score across most pages. Accessibility consistently passed. Performance scores overall did not pass on every page and is certainly something I will endeavor to improve in the future

![Home](./assets/testing-images/pp5lh.png)


## Manual Testing

- Home Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Navbar|Click on logo in Navbar|Redirect to Home |Pass|Navbar present on all pages |

- SWEETiS Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Pagination| Click on all of the links in the pagination. Ensure they redirect to the appropriate page. |All links redirect to the correct page. |Pass| |


- Sweet Details Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Sweet details|Open the product page. Ensure all the relevant information is correct for the specific product|All the relevant information is correct for the specific product|Pass||


- Bag 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Bag|Add product to bag and ensure it appears correctly in the bag|The product appears correctly in the bag|Pass||

- Checkout

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Checkout|Fill in the form and click on save details. Use stripe test card and confirm the order is successfull by checking stripe. Confirm the address is saved to profile|The address is saved to my profile. The purchase is successfull. Stripe logs show success.|Pass||

- User Profile

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Profile|Fill in the form and click on update. Ensure the details are updated|The details are updated|Pass||

- Orders

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Orders|Open the orders page and ensure the orders showing are correct. |The orders are correct|Pass||
|Orders |Click on the order link and ensure it leads to the order page|The link leads to the order page|Pass||

- Wishlist

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|wishlist|Visit my wishlist page. Click on the heart button on the card. Ensure the card is removed from favourites |The card is removed from favourites|Pass||
|wishlist|Visit my wishlist page. Click on the add to cart button on the card. Ensure the product is added to cart |The product is added to cart|Pass||
|wishlist|Visit my wishlist page. Click on the card. Ensure it redirects to the product's page. |It redirects to product's page|Pass||

- Admin

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Orders|Visit orders page. Ensure the refine drop down works by selecting all available options |The refine drop down works as expected|Pass||
|Discount code|Visit discount code page. Ensure the refine drop down works by selecting all available options |The refine drop down works as expected|Pass||


## User Story Testing

| **User Story** | **Description** | **Status** |
| --- | --- | --- |
| US - Project Setup | As a **developer** I can set up a new Django project so that I can establish the project structure. | ✅ |
| US - Storage Setup | As a **developer** I can connect the database and media storage so that user data and images are stored successfully. | ✅ |
| US - Early Deployment | As a **developer** I can deploy the application early so that I can verify everything works and continue testing during development. | ✅ |
| US - Homepage | As a **user** I can visit the homepage so I understand the purpose of Sweetiverse. | ✅ |
| US - Navigation | As a **user** I can navigate the website efficiently to access different sections like products, help, or cart. | ✅ |
| US - Browse Sweets | As a **user** I want to be able to view all available sweets so that I can browse and discover treats to purchase. | ✅ |
| US - Sweet Details | As a **user** I want to view detailed information about a single sweet so I can make informed decisions. | ✅ |
| US - Filter Sweets | As a **user** I want to filter sweets by country or category so I can find exactly what I’m interested in. | ✅ |
| US - Search Sweets | As a **user** I want to search for sweets by keywords so that I can quickly find specific items. | ✅ |
| US - Sort Sweets | As a **user** I want to sort the sweet list by name or price so I can easily compare options. | ✅ |
| US - Register | As a **user** I want to register an account so I can access full functionality. | ✅ |
| US - Login | As a **user** I want to log in to my account so I can personalize my experience. | ✅ |
| US - Password Reset | As a **user** I want to reset my password if I forget it so I can regain access. | ✅ |
| US - Profile Update | As a **user** I want to update my profile information so I can keep my account current. | ✅ |
| US - Submit Review | As an **authenticated user** I want to leave reviews for sweets so I can share feedback. | ✅ |
| US - Edit/Delete Review | As an **authenticated user** I want to edit or delete my reviews to keep them relevant. | ✅ |
| US - Wishlist | As an **authenticated user** I want to add sweets to my wishlist so I can save them for later. | ✅ |
| US - Add to Cart | As a **user** I want to add products to my cart so I can review them before purchase. | ✅ |
| US - Remove from Cart | As a **user** I want to remove items from my cart so I can adjust my order. | ✅ |
| US - Adjust Quantity | As a **user** I want to adjust the quantity of items in my cart for accurate purchasing. | ✅ |
| US - Apply Discount | As a **user** I want to apply discount codes to get deals and savings. | ✅ |
| US - Stripe Payment | As a **user** I want to securely pay for items using Stripe so I can complete purchases confidently. | ✅ |
| US - Smooth Checkout | As a **user** I want to complete checkout easily so I can buy sweets without friction. | ✅ |
| US - Admin Dashboard | As an **admin** I want to view an admin dashboard to monitor orders and activity. | ✅ |
| US - Manage Inventory | As an **admin** I want to add, update, or delete sweets so I can manage the inventory. | ✅ |
| US - Adjust Stock | As an **admin** I want to adjust stock levels to maintain availability. | ✅ |
| US - Submit Testimonial | As a **user** I want to submit a testimonial about my experience to share feedback. | ✅ |
| US - View Testimonials | As a **user** I want to read other users’ testimonials to build trust. | ✅ |
| US - Newsletter Signup | As a **user** I want to sign up for a newsletter so I can stay updated with offers. | ✅ |
| US - SEO Optimization | As the **site owner** I want the site to be SEO optimized so Sweetiverse ranks higher and attracts more users. | ✅ |
