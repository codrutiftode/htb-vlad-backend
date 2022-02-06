import math
import os
from flask import Flask
from flask import json
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)

@app.route('/api/hello')
def api():
    return "Hey"

# Returns a list of ingredients for a recipe
def parseRecipeIngredients(recipe):
    ingredients = recipe['ingredients'].copy()
    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i].split(" ")[1:]
        ingredients[i] = ' '.join(ingredients[i])
    return ingredients


# Returns the ranks for each recipe based on relevance to a list of ingredients
def getRecipeRanks(ingredients, recipes):
    ranks = [0 for i in range(len(recipes))]
    for r in range(len(ranks)):
        rank = 0
        parsedIngredients = parseRecipeIngredients(recipes[r])
        for ingredient in ingredients:
            for i in parsedIngredients:
                if ingredient in i:
                    rank += 1
        ranks[r] = rank
    return ranks


# returns a list of recipes catered to a list of ingredients
@app.route('/api/getRecipesFromIngredients')
@cross_origin()
def getRecipesFromIngredients():
    ingredients = request.args.getlist('ingredients')
    ranks = getRecipeRanks(ingredients, allRecipes)
    recipes = allRecipes
    recipe_rank_tuples=[(recipes[i],ranks[i]) for i in range(len(ranks))]
    for i in range(0,len(recipe_rank_tuples)-1):  
        for j in range(len(recipe_rank_tuples)-1):  
            if(recipe_rank_tuples[j][1]>recipe_rank_tuples[j+1][1]):  
                temp = recipe_rank_tuples[j]  
                recipe_rank_tuples[j] = recipe_rank_tuples[j+1]  
                recipe_rank_tuples[j+1] = temp  
    final_recipes = [t[0] for t in recipe_rank_tuples if t[1] > 0]
    final_recipe_titles = []
    recipes_to_return = []
    for recipe in final_recipes:
        if recipe["title"] not in final_recipe_titles:
            final_recipe_titles.append(recipe["title"])
            recipes_to_return.append(recipe)
    pruneDiet(recipes_to_return)
    return jsonify(recipes_to_return)
    
@app.route('/api/sendDiet', methods = ['GET'])
@cross_origin()
def sendDiet():
    global diet
    diet = request.args.getstring('diet')

def pruneDiet(initialRecipes):
    sentDiet = diet
    recipes_to_return = []
    if sentDiet == None:
        return initialRecipes
    for recipe in initialRecipes:
        if recipe["diet"] == sentDiet:
            recipes_to_return.append(recipe)
    return recipes_to_return


# returns a list of ingredient objects
@app.route('/api/getAllIngredients')
@cross_origin()
def getAllIngredients():
    global allIngredients
    filename = os.path.join(app.static_folder, './data/ingredients.json')
    with open(filename) as ingredients_file:
        allIngredients = json.load(ingredients_file)
    return jsonify(allIngredients)


###---- INITIALISING JSON FILES FOR INGREDIENTS AND RECIPES ----###
def initIngredients():
    global allIngredients
    filename = os.path.join(app.static_folder, './data/ingredients.json')
    with open(filename) as ingredients_file:
        allIngredients = json.load(ingredients_file)

def initRecipes():
    global allRecipes
    filename = os.path.join(app.static_folder, './data/recipes.json')
    with open(filename) as recipes_file:
        allRecipes = json.load(recipes_file)


initIngredients()
initRecipes()

###-------------------------------------------------------------###


# returns the whole ingredient object, given its ID (ingredients.json)
@app.route('/api/getIngredientObj/<id>', methods = ['GET', 'POST'])
def getIngredientObj(id):
    id = int(id)
    categories = allIngredients['Categories']
    for cat in categories:
        if cat['id'] == math.floor(id / 100):
            for ingredient in cat['ingredients']:
                if ingredient['id'] == id:
                    return ingredient


# returns the whole recipe object, given its ID (recipes.json)
@app.route('/api/getRecipeObj/<id>', methods = ['GET', 'POST'])
def getRecipeObj(id):
    id = int(id)
    for r in allRecipes:
        if r['id'] == id:
            return str(r['ingredients'])
        else:
            return ""


# returns a title of an ingredient, given its ID
@app.route('/api/getIngredientName/<id>', methods = ['GET', 'POST'])
def getIngredientName(id):
    return (getIngredientObj(id))['title']


# returns a list of ingredients, given a recipe ID
@app.route('/api/getRecipeIngredients/<id>', methods = ['GET', 'POST'])
def getRecipeIngredients(id):
    return (getRecipeObj(id))['ingredients']


@app.route('/')
def home():
    return 'Home Page Route'


@app.route('/about')
def about():
    return 'About Page Route'


@app.route('/portfolio')
def portfolio():
    return 'Portfolio Page Route'


@app.route('/contact')
def contact():
    return 'Contact Page Route'

# Run the application
if __name__ == '__main__':
    app.run()
