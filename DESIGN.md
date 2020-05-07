# DESIGN DOCUMENTATION

## Homepage

Because the goal of the website is to be very accessible to users, I went ahead and displayed all the information for the menu of the day on the homepage. I picked one of the set bootstrap themes and applied it to the site. I assigned each menu (soup of the day, lunch, and dinner) a different card with a different color to make it easier to separate the three/easier to read.


## How the menu was extracted

The CS50 HUDS API was increadibly helpful in making it easier to extract the different menu parts. To make it easier to repeatedly call on the API with different variable specifications, I made multiple functions that will let me get the soup of the day, all the lunch entrees, lunch desserts, dinner entrees, and dinner desserts. Here are the different functions I created:

### menu(date, category, meal) and food(recipe)
These two functions work together -- the first one extracts the recipe, and the second extracts the different item names in the list. I made sure to include the date, category, and meal parameters because these are the main ones that are being manipulated in the website.

### get_() i.e., get_soup(date), get_lunch(date), etc.

All the get_ functions only have one parameter: the date. This is because the date is the only variable that is being constantly changed everyday. The category id for soup, for example, is constant. So, it was easier to just define different functions like get_soup() because it calles on two other functions -- menu() and food() -- each time. This just made coding more efficient on my end.

## Menu for the week

Because the menu for the day has the same layout -- but different dates! -- than the rest of the week, it was easier to just make different html pages for each of the day of the week. This also allowed me to make a python for loop that stores the different menu items in a list so that it was easier to call on in each of those html pages.

## Ratings page

I made the ratings page only accessible by users to deter randos from just rating the meals and spamming the website.

All results are currently internal because there are not enough users using the ratings page, so any data displayed will be incredibly inaccurate. In the future, data results will definitely be displayed.