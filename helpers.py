import requests
import urllib.parse
import requests
import json

from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime
from urllib.request import urlopen


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        response = requests.get(f"https://api.iextrading.com/1.0/stock/{urllib.parse.quote_plus(symbol)}/quote")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def unique(x):
    """Remove duplicates in list"""
    return list(dict.fromkeys(x))

# api-endpoint
url_locations = "https://api.cs50.io/dining/locations"
url_categories = "https://api.cs50.io/dining/categories"
url_recipes = "https://api.cs50.io/dining/recipes"
url_menus = "https://api.cs50.io/dining/menus"

# menu categories
# {"id": 2, "name": "Breakfast Entrees"}, {"id": 7, "name": "Today's Soup"}, {"id": 9, "name": "Brunch"}
# {"id": 12, "name": "Entrees"}, {"id": 13, "name": "Vegetarian Entree"}, {"id": 14, "name": "Starch And Potatoes"}
# {"id": 17, "name": "Desserts"}, {"id": 28, "name": "Bistro Bowl"}, {"id": 60, "name": "Entrees"}

# menu meal
# {"id": 0, "name": "Breakfast"}, {"id": 1, "name": "Lunch"}, {"id": 2, "name": "Dinner"}

def menu(date, category, meal):
    """Segment the menu JSON based on category and meal type."""
    url = url_menus + "?" + "date={}".format(date) + "&category={}".format(category) + "&meal={}".format(meal)
    obj = urlopen(url)
    js = obj.read().decode('utf-8')
    load = json.loads(js)
    return load

def food(recipe):
    """Loop through results to extract dish names."""
    dishes = []
    for item in recipe:
        x = str(item["recipe"])
        recipe_url = "https://api.cs50.io/dining/recipes/"
        url = recipe_url + x
        obj = urlopen(url)
        js = obj.read().decode('utf-8')
        load = json.loads(js)
        dish = load["name"]
        dishes.append(dish)
    return dishes

def get_soup(date):
    """Get the Soup of the Day"""
    recipe_soup = menu(date=date, category=7, meal=1)
    soup = food(recipe_soup)
    return(soup)

def get_lunch(date):
    """Extract all the Lunch Entrees"""

    # Find the current day
    day = date.strftime('%A')

    # combine all the different kinds of entrees
    recipe_entree = menu(date, category=12, meal=1)
    entree = food(recipe_entree)

    recipe_veg_entree = menu(date, category=13, meal=1)
    veg_entree = food(recipe_veg_entree)

    recipe_potat = menu(date, category=14, meal=1)
    potat = food(recipe_potat)

    if day == "Sunday":
        recipe_brunch = menu(date, category=9, meal=1)
        brunch = food(recipe_brunch)
        dishes = brunch
    else:
        dishes = entree + veg_entree + potat
    return dishes

def get_dinner(date):
    """Extract all the Dinner Entrees"""

    # Find the current day
    day = date.strftime('%A')

    # combine all the different kinds of entrees
    recipe_entree = menu(date, category=12, meal=2)
    entree = food(recipe_entree)

    recipe_veg_entree = menu(date, category=13, meal=2)
    veg_entree = food(recipe_veg_entree)

    recipe_potat = menu(date, category=14, meal=2)
    potat = food(recipe_potat)

    if day == "Thursday":
        recipe_bistro = menu(date, category=28, meal=2)
        bistro = food(recipe_bistro)
        dinner = bistro + entree + veg_entree + potat
    else:
        dinner = entree + veg_entree + potat
    return dinner

def get_dessert(date, meal):
    """Get Dessert of a Meal"""
    recipe_dessert = menu(date=date, category=17, meal=meal)
    dessert = food(recipe_dessert)
    return(dessert)