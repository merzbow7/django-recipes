manage="poetry run python manage.py"

poetry run python -m pip install --upgrade pip
$manage collectstatic --noinput
$manage flush --no-input
$manage makemigrations
$manage migrate
#$manage loaddata ingredientname ingredient recipe
$manage initadmin
$manage runserver 0.0.0.0:8000
