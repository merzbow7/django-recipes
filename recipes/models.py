from django.db import models

# Create your models here.
from django.urls import reverse


class IngredientName(models.Model):
    name = models.CharField(max_length=255, blank=False, db_index=True)

    def __str__(self):
        return f"{self.name}"


class Ingredient(models.Model):
    count = models.CharField(max_length=25, blank=False)
    name = models.ForeignKey(IngredientName, on_delete=models.PROTECT)

    class Meta:
        app_label = 'recipes'
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return f"{self.name.name} - {self.count}"


class Recipe(models.Model):
    title = models.CharField(max_length=255, blank=False, db_index=True)
    description = models.TextField()
    cooking = models.TextField()
    slug = models.SlugField(max_length=255, blank=True)
    ingredients = models.ManyToManyField(Ingredient)

    class Meta:
        app_label = 'recipes'
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f"{self.title}"

    def delete(self, using=None, keep_parents=False):
        ingredients = self.ingredients.all()
        print(f"{ingredients=}")
        for ing in ingredients:
            print(ing)
            ing.delete()
        super(Recipe, self).delete()

    def get_absolute_url(self):
        return reverse('recipe_url', kwargs={'slug': self.slug})
