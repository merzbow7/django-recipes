from django import forms

from recipes.models import Recipe, IngredientName, Ingredient


class RecipeForm(forms.ModelForm):
    ingredients_list = forms.CharField(
        widget=forms.Textarea,
        help_text="Enter the ingredients through a dash",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.prepopulate_ingredients()

    def prepopulate_ingredients(self):
        """Fill ingredients field."""
        list_ings = self.get_list_ings()
        self.fields['ingredients_list'].initial = "\n".join(list_ings)

    def get_list_ings(self):
        """Get ingredients list of current recipe."""
        ings = self.instance.ingredients.all()
        return [f"{ing.name} - {ing.count}" for ing in ings]

    @staticmethod
    def create_ing_name(name):
        """Create instance of IngredientName."""
        return IngredientName.objects.get_or_create(ing_name=name)[0]

    def create_ings_obj(self, ing_id, count):
        """Create instance of Ingredient."""
        ing = Ingredient.objects.get_or_create(
            name_id=ing_id.id,
            count=count
        )
        return ing[0]

    def create_ings(self, ingredients):
        """Create list of Ingredient."""
        ings_obj_list = []

        for ing in ingredients:
            ing_name = self.create_ing_name(ing[0].strip())
            ing_obg = self.create_ings_obj(ing_name, ing[1].strip())
            ings_obj_list.append(ing_obg)

        return ings_obj_list

    @staticmethod
    def get_ings_list(ingredients_text):
        """Split text of ingredients to list of tuple."""
        ings = []
        split_text = map(str.strip, ingredients_text.split('\n'))

        for ingredient in split_text:
            split = ingredient.split('-', maxsplit=1)
            if len(split) == 2:
                ings.append(split)

        return ings

    def del_ings(self, ingredients):
        """Remove Ingredients from Recipe."""
        exiting_ings = self.instance.ingredients.all()
        delete_ings = [ing for ing in exiting_ings if ing not in ingredients]
        self.instance.ingredients.remove(*delete_ings)
        for ing in delete_ings:
            ing.delete()

    def save_ings(self, ingredients):
        """Save Ingredients to Recipe."""
        self.instance.ingredients.add(*ingredients)

    def save(self, commit=True):
        recipe = super(RecipeForm, self).save(commit=commit)
        if not recipe.id:
            recipe.save()

        ings_text = self.cleaned_data.get('ingredients_list', None)
        ings_list = self.get_ings_list(ings_text)
        ings = self.create_ings(ings_list)

        self.del_ings(ings)
        self.save_ings(ings)
        self.instance.save()

        return recipe

    class Meta:
        model = Recipe
        fields = '__all__'
