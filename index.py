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


# @app.route('/api')
# def api():
#     with open('data.json', mode='r') as my_file:
#         text = my_file.read()
#         return text

def parseRecipeIngredients(recipe):
    ingredients = recipe['ingredients'].copy()
    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i].split(" ")[1:]
        ingredients[i] = ' '.join(ingredients[i])
    return ingredients


#@app.route('/api/getRecipeRanks/<ingredients>')
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

@app.route('/api/getRecipesFromIngredients')
@cross_origin()
def getRecipesFromIngredients():
    # ingredients = ingredientString.split("&")
    ingredients = request.args.getlist('ingredients')
    ranks = getRecipeRanks(ingredients, allRecipes)
    recipes = allRecipes
    recipe_rank_tuples=[(recipes[i],ranks[i]) for i in range(len(ranks))]
    # bubble sort
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
    return jsonify(recipes_to_return)
    


@app.route('/api/getAllIngredients')
@cross_origin()
def getAllIngredients():
    global allIngredients
    filename = os.path.join(app.static_folder, './data/ingredients.json')
    with open(filename) as ingredients_file:
        allIngredients = json.load(ingredients_file)
        
    return jsonify(allIngredients)


"""
@app.route('/api/getRecipes/<idArray>', methods = ['GET', 'POST'])
def getRecipes(idArray):
    ignts = getAllIngredients()


@app.route('/api/getIngredients/<idArray>', methods = ['GET', 'POST'])
def getIngredients(idArray):
    recipeArray = []
    for i in idArray:
        if allIngredients['Categories']['id':1]['id'].values() == i:
            recipeArray.append(getIngredientObj(i))
    return recipeArray
"""

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





    """
    if allIngredients['Categories']['id':math.floor(id/100)]['id'].values() == id:
        return allIngredients['Categories']['id':math.floor(id/100)]['id':id]
    else:
        return {}
        """



# stupid:
"""
@app.route('/api/selectIngredients', methods = ['GET'])
def selectIngredients():
    selectedIngredients = request.args.getlist('ingredients')
    getRecipes(selectedIngredients)

@app.route('/api/getRecipes')   ## add helper function getIngIndex()
def getRecipes(selectedIngredients):
    allIngIndex = getIngIndex()
    
@app.route('/api/getIngIndex')
def getIngIndex():
    global allRecipes
    filename = os.path.join(app.static_folder, './data/recipes.json')
    with open(filename) as recipes_file:
        allRecipes = json.load(recipes_file)
    return allRecipes       ## change this, needs to be usable data type, or change later
"""
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
