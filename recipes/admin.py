from django.contrib import admin

from recipes.models import Ingredient, IngredientUnit, Recipe
from recipes.recipe_form import RecipeForm

admin.AdminSite.site_header = 'Django Admin Recipes'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(IngredientUnit)
class IngredientUnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'description', 'ingredients_list', 'cooking', 'slug')

    form = RecipeForm
