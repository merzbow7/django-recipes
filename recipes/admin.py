from django.contrib import admin
from django.contrib.admin import AdminSite

from .forms import RecipeForm
from .models import Recipe

AdminSite.site_header = "Django Admin Recipes"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'description', 'ingredients_list', 'cooking', 'slug')

    form = RecipeForm
