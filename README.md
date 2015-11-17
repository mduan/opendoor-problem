# Instructions #

Access the API at http://opendoor-problem.herokuapp.com/listings.

Supports the following query parameters:

- **min_price**: The minimum listing price in dollars.
- **max_price**: The maximum listing price in dollars.
- **min_bed**: The minimum number of bedrooms.
- **max_bed**: The maximum number of bedrooms.
- **min_bath**: The minimum number of bathrooms.
- **max_bath**: The maximum number of bathrooms.
- **page**: The current page of listings we are showing. Default is 0.
- **results_per_page**: The number of listings to show per page. Default is 100.

Following is a example query with the parameters set: http://opendoor-problem.herokuapp.com/listings?min_price=100000&max_price=200000&min_bed=2&max_bed=2&min_bath=2&max_bath=2&page=1&results_per_page=50

# Potential improvements #
- Store the listings in a database and create indices for the query parameters (excluding page and results_per_page).
These indices will optimize the filtering vs. the manual filtering I'm currently doing. Furthermore, the pagination
I implemented requires re-iterating over items from previous pages. Databases are also optimized for retrieving
items from an offset which could be used to implement pagination more efficiently.
