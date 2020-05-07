import json
from urllib.request import urlopen

## GET HUDS JSON DATA
# api-endpoint
url_locations = "https://api.cs50.io/dining/locations"
url_categories = "https://api.cs50.io/dining/categories"
url_recipes = "https://api.cs50.io/dining/recipes"
url_menus = "https://api.cs50.io/dining/menus"

# SEND GET REQUEST AND SAVE RESPONSE AS RESPONSE OBJECT
obj_locations = urlopen(url_locations)
obj_categories = urlopen(url_categories)
obj_recipes = urlopen(url_recipes)
obj_menus = urlopen(url_menus)

# EXTRACTING DATA IN JSON FORMAT
json_locations = obj_locations.read().decode('utf-8')
json_categories = obj_categories.read().decode('utf-8')
json_recipes = obj_recipes.read().decode('utf-8')
json_menus = obj_menus.read().decode('utf-8')

locations = json.loads(json_locations)
categories = json.loads(json_categories)
recipes = json.loads(json_recipes)
menus = json.loads(json_menus)

# EXTRACTING A SPECIFIC VALUE
print("Meal: ", menus[0]['meal'])

