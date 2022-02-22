from django.db import models
from django.urls import reverse


class Ingredient(models.Model):
    name = models.CharField(max_length=255, blank=False, db_index=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        app_label = 'recipes'
        verbose_name = 'Ingredient name'
        verbose_name_plural = 'Ingredients name'


class Recipe(models.Model):
    title = models.CharField(max_length=255, blank=False, db_index=True)
    description = models.TextField()
    cooking = models.TextField()
    slug = models.SlugField(max_length=255, blank=True)
    recipe_ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
    )

    class Meta:
        app_label = 'recipes'
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('recipe_url', kwargs={'slug': self.slug})


class RecipeIngredient(models.Model):
    amount = models.CharField(max_length=25, blank=False)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        app_label = 'recipes'
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return f'{self.ingredient.name}-{self.amount}'
