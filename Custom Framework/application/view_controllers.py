import json

from database_models import Recipe
from framework.templates_handler import redirect_to_path, render_template
from playhouse.shortcuts import model_to_dict


def insert_recipes(request):
    error = None
    respond = {
        "name": "",
        "difficulty": "",
        "description": "",
        "ingredients": "",
    }

    if request.method == 'POST':
        respond["name"] = request.form['name']
        respond["difficulty"] = request.form['difficulty']
        respond["ingredients"] = request.form['ingredients']
        respond["description"] = request.form['description']
        Recipe.create(**respond)
        return redirect_to_path("/")
    return render_template(
        'insert_record.html',
        error=error,
        **respond
    )


def get_recipes(request):
    recipes = Recipe.select()
    data = []
    for recipe in recipes:
        data.append(model_to_dict(recipe))
    if data:
        data = json.dumps(data)
    return render_template(
        'get_record.html', data=data)
