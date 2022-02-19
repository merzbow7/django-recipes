from django import forms

from recipes.models import Recipe, Ingredient, RecipeIngredient


class RecipeForm(forms.ModelForm):
    ingredients_list = forms.CharField(
        widget=forms.Textarea,
        help_text="Enter the ingredients through a dash",
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.prepopulate_ingredients()

    def prepopulate_ingredients(self) -> None:
        """Fill ingredients field."""
        list_ings = self.get_list_ings()
        self.fields['ingredients_list'].initial = "\n".join(list_ings)

    def get_list_ings(self) -> list[str]:
        """Get ingredients list of current recipe."""
        self.instance: Recipe
        ings = self.instance.recipeingredient_set.all()
        return [f"{ing.name.name} - {ing.amount}" for ing in ings]

    @staticmethod
    def create_ing_name(name: str) -> Ingredient:
        """Create instance of IngredientName."""
        return Ingredient.objects.get_or_create(
            name=name
        )[0]

    def create_ings_obj(self, name: str, amount: str) -> RecipeIngredient:
        """Create instance of Ingredient."""
        name_ing = self.create_ing_name(name)
        ingredient = RecipeIngredient.objects.get_or_create(
            amount=amount, recipe=self.instance, name=name_ing
        )[0]

        return ingredient

    def create_ings(self, ingredients):
        """Create list of Ingredient."""
        ingredients_obj = []
        for item in ingredients:
            ing = map(str.strip, item)
            ingredients_obj.append(self.create_ings_obj(*ing))

        return ingredients_obj

    @staticmethod
    def get_ings_list(ingredients_text: str) -> list[list[str, str]]:
        """Split text of ingredients to list of tuple."""
        ings = []
        split_text = map(str.strip, ingredients_text.split('\n'))

        for ingredient in split_text:
            split = ingredient.split('-', maxsplit=1)
            if len(split) == 2:
                ings.append(split)

        return ings

    def del_ings(self, ingredients: list[RecipeIngredient]) -> None:
        """Remove Ingredients from Recipe."""
        exiting_ings = self.instance.recipeingredient_set.all()
        delete_ings = [ing for ing in exiting_ings if ing not in ingredients]
        for ing in delete_ings:
            ing.delete()

    def save_ings(self, ingredients):
        """Save Ingredients to Recipe."""
        self.instance.ingredients.add(*ingredients)

    def save(self, commit=True):
        recipe = super(RecipeForm, self).save(commit=commit)
        if not self.instance.id:
            recipe.save()

        ings_text = self.cleaned_data.get('ingredients_list', None)
        ings_list = self.get_ings_list(ings_text)
        created = self.create_ings(ings_list)
        self.del_ings(created)

        return recipe

    class Meta:
        model = Recipe
        fields = '__all__'
