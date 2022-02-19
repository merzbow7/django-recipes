manage="poetry run python manage.py"

poetry install --no-dev
$manage migrate
$manage loaddata ingredient recipeingredient recipe
$manage initadmin
$manage runserver 0.0.0.0:8000
