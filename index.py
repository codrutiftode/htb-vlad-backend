import os
from flask import Flask
from flask import json
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

@app.route('/api/getAllIngredients')
def getAllIngredients():
    global allIngredients
    filename = os.path.join(app.static_folder, './data/ingredients.json')
    with open(filename) as ingredients_file:
        allIngredients = json.load(ingredients_file)
    return allIngredients

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