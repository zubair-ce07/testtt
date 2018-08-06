**Lastcall Website Scrapped**

1. parse_homepage to select all categories
2. parse_category_page have 3 parts
   a. handle items on that page
   b. handle subcategories of that category not on main page
   c. handle pagination for that category
3. category_params_data to genrate the form data for the post request of pagination
4. parse_item_page to handle the return of post requst form pagination
5. parse_item to extract all the information about the item
6. parse_color to extract the color and size info from the response of the post request
7. extract_image_urls to extract the image urls for all the images associated to the image

