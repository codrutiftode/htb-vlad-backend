def parseRecipeIngredients(recipe):
    ingredients = recipe['ingredients']
    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i].split(" ")[1:]
        ingredients[i] = ' '.join(ingredients[i])
    return ingredients


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