poetry run python manage.py dumpdata recipes.ingredientname --indent 2 -o ingredientname.json
poetry run python manage.py dumpdata recipes.ingredient --indent 2 -o ingredient.json
poetry run python manage.py dumpdata recipes.recipe --indent 2 -o recipes.recipe.json
