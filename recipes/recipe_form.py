"""Admin form for Recipe."""
import re
from collections.abc import Iterable
from typing import NamedTuple

from django import forms

from recipes.models import Ingredient, IngredientUnit, Recipe, RecipeIngredient


class TIngredient(NamedTuple):
    """Parsed Ingredient from text field."""

    name: str = ''
    amount: str = ''
    unit: str = ''


IngredientList = list[TIngredient]


def strip_text(iterable: Iterable) -> Iterable:
    """Strip text in Iterable."""
    return tuple(map(str.strip, iterable))


def create_ing_name(name: str) -> Ingredient:
    """Create instance of IngredientName."""
    ingredient = Ingredient.objects.get_or_create(
        name=name,
    )
    return ingredient[0]


def del_ingredients(ingredients: list[Ingredient]) -> None:
    """Remove ingredients."""
    for ing in ingredients:
        links = ing.recipeingredient_set.count()
        if links == 0:
            ing.delete()


def create_unit(name):
    """Create instance of IngredientUnit."""
    return IngredientUnit.objects.get_or_create(name=name)[0]


def get_ingredients_list(ingredients_text: str) -> IngredientList:
    """Split text of ingredients to list of tuple."""
    ings = []
    split_text = strip_text(ingredients_text.split('\n'))

    for ingredient in split_text:
        split_text = re.split('[:_]', ingredient)
        if 2 <= len(split_text) < 4:
            ings.append(TIngredient(*strip_text(split_text)))
    return ings


class RecipeForm(forms.ModelForm):
    ingredients_list = forms.CharField(
        widget=forms.Textarea,
        help_text='Enter the ingredients through a dash',
        label='List of ingredients',
    )

    def __init__(self, *args, **kwargs) -> None:
        """Create form and fill ingredients."""
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.prepopulate_ingredients()

    def prepopulate_ingredients(self) -> None:
        """Fill ingredients field."""
        list_ings = self.get_ingredients_text()
        self.fields['ingredients_list'].initial = '\n'.join(list_ings)

    def get_ingredients_text(self) -> list[str]:
        """Get ingredients list of current recipe."""
        self.instance: Recipe
        ingredients = self.instance.recipeingredient_set.all()
        ingredient_text_list = []

        for ingredient in ingredients:
            underscore = '_' if ingredient.unit_id.name else ''

            ingredient_str = (
                ingredient.ingredient_id.name,
                ': ',
                ingredient.amount,
                underscore,
                ingredient.unit_id.name,
            )

            ingredient_text_list.append(''.join(ingredient_str))

        return ingredient_text_list

    def create_ingredient_obj(
        self, ingredient: TIngredient,
    ) -> RecipeIngredient:
        """Create instance of Ingredient."""
        name_ing = create_ing_name(ingredient.name)
        unit = create_unit(ingredient.unit)
        ingredient = RecipeIngredient.objects.get_or_create(
            amount=ingredient.amount,
            recipe_id=self.instance,
            ingredient_id=name_ing,
            unit_id=unit,
        )

        return ingredient[0]

    def create_ingredients(self, ingredients) -> list[RecipeIngredient]:
        """Create list of Ingredient."""
        ingredients_obj = []
        for ingredient in ingredients:
            ingredient_object = self.create_ingredient_obj(ingredient)
            ingredients_obj.append(ingredient_object)
        return ingredients_obj

    def del_recipe_ingredients(
        self, ingredients: list[RecipeIngredient],
    ) -> list[Ingredient]:
        """Remove Ingredients from Recipe."""
        exiting_ings = self.instance.recipeingredient_set.all()
        delete_ings = [ing for ing in exiting_ings if ing not in ingredients]
        for_delete = []

        for ing in delete_ings:
            links = ing.ingredient_id.recipeingredient_set.count()
            if links == 1:
                for_delete.append(ing.ingredient_id)
            ing.delete()

        return for_delete

    def save(self, commit=True):
        """Save form and process ingredients to models."""
        recipe = super().save(commit=commit)
        if not self.instance.id:
            recipe.save()

        ingredients_text = self.cleaned_data.get('ingredients_list', None)
        ingredients_list = get_ingredients_list(ingredients_text)
        created_ingredients = self.create_ingredients(ingredients_list)
        remove_ingredients = self.del_recipe_ingredients(created_ingredients)
        del_ingredients(remove_ingredients)

        return recipe

    class Meta:
        model = Recipe
        fields = '__all__'
