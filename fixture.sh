dump="poetry run python manage.py dumpdata"

#$dump recipes.ingredientname --indent 2 -o ingredientname.json
$dump recipes.ingredient --indent 2 -o ingredient.json
$dump recipes.recipe --indent 2 -o recipes.recipe.json
