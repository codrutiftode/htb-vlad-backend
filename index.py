import math
import os
from flask import Flask
from flask import json
from flask import jsonify
from flask import request


app = Flask(__name__)

@app.route('/api/hello')
def api():
    return "Hey"


# @app.route('/api')
# def api():
#     with open('data.json', mode='r') as my_file:
#         text = my_file.read()
#         return text

def parseRecipeIngredients(recipe):
    ingredients = recipe['ingredients']
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


@app.route('/api/getRecipesFromIngredients/<ingredientString>', methods=['GET', 'POST'])
def getRecipesFromIngredients(ingredientString):
    return ingredientString


@app.route('/api/getAllIngredients')
def getAllIngredients():
    global allIngredients
    filename = os.path.join(app.static_folder, './data/ingredients.json')
    with open(filename) as ingredients_file:
        allIngredients = json.load(ingredients_file)
        
    response = jsonify(allIngredients)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


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


@app.route('/api/getIngredientObj/<id>', methods = ['GET', 'POST'])
def getIngredientObj(id):
    id = int(id)
    categories = allIngredients['Categories']
    for cat in categories:
        if cat['id'] == math.floor(id / 100):
            for ingredient in cat['ingredients']:
                if ingredient['id'] == id:
                    return ingredient


@app.route('/api/getRecipeObj/<id>', methods = ['GET', 'POST'])
def getRecipeObj(id):
    id = int(id)
    for r in allRecipes:
        if r['id'] == id:
            return str(r['ingredients'])
        else:
            return ""


# returns a title of an ingrediant, given its ID
@app.route('/api/getIngredientName/<id>', methods = ['GET', 'POST'])
def getIngredientName(id):
    return (getIngredientObj(id))['title']


# 
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
