"""Admin form for Recipe."""

from collections.abc import Iterable

from django import forms

from recipes.models import Recipe, Ingredient, RecipeIngredient


def strip_text(iterable: Iterable) -> Iterable:
    return map(str.strip, iterable)


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


class RecipeForm(forms.ModelForm):
    ingredients_list = forms.CharField(
        widget=forms.Textarea,
        help_text='Enter the ingredients through a dash',
        label='List of ingredients',
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.prepopulate_ingredients()

    def prepopulate_ingredients(self) -> None:
        """Fill ingredients field."""
        list_ings = self.get_list_ings()
        self.fields['ingredients_list'].initial = '\n'.join(list_ings)

    def get_list_ings(self) -> list[str]:
        """Get ingredients list of current recipe."""
        self.instance: Recipe
        ings = self.instance.recipeingredient_set.all()
        return [f'{ing.name.name} - {ing.amount}' for ing in ings]

    def create_ings_obj(self, name: str, amount: str) -> RecipeIngredient:
        """Create instance of Ingredient."""
        name_ing = create_ing_name(name)
        ingredient = RecipeIngredient.objects.get_or_create(
            amount=amount,
            recipe=self.instance,
            name=name_ing,
        )

        return ingredient[0]

    def create_ings(self, ingredients) -> list[RecipeIngredient]:
        """Create list of Ingredient."""
        ingredients_obj = []
        for ingredients in ingredients:
            ing = strip_text(ingredients)
            ingredients_obj.append(self.create_ings_obj(*ing))

        return ingredients_obj

    def get_ings_list(self, ingredients_text: str) -> list[list[str, str]]:
        """Split text of ingredients to list of tuple."""
        ings = []
        split_text = strip_text(ingredients_text.split('\n'))

        for ingredient in split_text:
            split = ingredient.split('-', maxsplit=1)
            if len(split) == 2:
                ings.append(split)

        return ings

    def del_recipe_ingredients(
            self, ingredients: list[RecipeIngredient],
    ) -> list[Ingredient]:
        """Remove Ingredients from Recipe."""
        exiting_ings = self.instance.recipeingredient_set.all()
        delete_ings = [ing for ing in exiting_ings if ing not in ingredients]
        for_delete = []

        for ing in delete_ings:
            links = ing.name.recipeingredient_set.count()
            if links == 1:
                for_delete.append(ing.name)
            ing.delete()

        return for_delete

    def save_ings(self, ingredients) -> None:
        """Save Ingredients to Recipe."""
        self.instance.ingredients.add(*ingredients)

    def save(self, commit=True):
        recipe = super().save(commit=commit)
        if not self.instance.id:
            recipe.save()

        ingredients_text = self.cleaned_data.get('ingredients_list', None)
        ingredients_list = self.get_ings_list(ingredients_text)
        created_ingredients = self.create_ings(ingredients_list)
        remove_ingredients = self.del_recipe_ingredients(created_ingredients)
        del_ingredients(remove_ingredients)

        return recipe

    class Meta:
        model = Recipe
        fields = '__all__'
