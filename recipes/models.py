from django.db import models

# Create your models here.
from django.urls import reverse


class IngredientName(models.Model):
    ing_name = models.CharField(max_length=255, blank=False, db_index=True)

    def __str__(self):
        return f"{self.ing_name}"


class Ingredient(models.Model):
    name = models.ForeignKey(IngredientName, on_delete=models.CASCADE)
    count = models.CharField(max_length=25, blank=False)

    class Meta:
        app_label = 'recipes'
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return f"{self.name.ing_name}"


class Recipe(models.Model):
    title = models.CharField(max_length=255, blank=False, db_index=True)
    description = models.TextField()
    cooking = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, blank=True)
    slug = models.SlugField(max_length=255, blank=True)

    class Meta:
        app_label = 'recipes'
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('recipe_url', kwargs={'slug': self.slug})
