dump="poetry run python manage.py dumpdata"
destination="recipes/fixtures"

$dump recipes.ingredient --indent 2 -o $destination/ingredient.json
$dump recipes.recipeingredient --indent 2 -o $destination/recipeingredient.json
$dump recipes.recipe --indent 2 -o $destination/recipe.json
