from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Recipe, Ingredient, IngredientName

AdminSite.site_header = "Django Admin Recipes"


@admin.register(IngredientName)
class IngredientNameAdmin(admin.ModelAdmin):
    extra_field = forms.CharField()


class IngredientAdmin(admin.TabularInline):
    model = Ingredient
    extra = 1
    save_on_top = True


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [IngredientAdmin]
