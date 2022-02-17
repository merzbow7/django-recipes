poetry run python -m pip install --upgrade pip
poetry run python manage.py collectstatic --noinput
poetry run python manage.py flush
poetry run python manage.py makemigrations
poetry run python manage.py migrate
#poetry run python manage.py loaddata ingredientname ingredient recipe
poetry run python manage.py initadmin
poetry run python manage.py runserver 0.0.0.0:8000
