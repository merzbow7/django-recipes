from contextlib import suppress

from django import forms

from recipes.models import Recipe, IngredientName, Ingredient


class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(
        widget=forms.Textarea,
        help_text="Enter the ingredients through a dash",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prepopulate_ingredients()

    def prepopulate_ingredients(self):
        list_ings = self.get_list_ings()
        self.fields['ingredients'].initial = "\n".join(list_ings)

    def get_list_ings(self):
        ings = self.instance.ingredients.all()
        return [f"{ing.name} - {ing.count}" for ing in ings]

    @staticmethod
    def create_ing_name(name):
        return IngredientName.objects.get_or_create(ing_name=name)[0]

    @staticmethod
    def create_ings_obj(ing_id, count, fk):
        ing = Ingredient.objects.get_or_create(
            name_id=ing_id.id,
            count=count,
            recipe_id=fk
        )

        print(ing_id.id)
        return ing[0]

    def create_ings(self, ingredients, recipe_id):
        ings_obj_list = []

        for ing in ingredients:
            name = ing.strip()
            count = ingredients[ing].strip()
            ing_name = self.create_ing_name(name)
            ing_obg = self.create_ings_obj(ing_name, count, fk=recipe_id)
            ings_obj_list.append(ing_obg)

        return ings_obj_list

    @staticmethod
    def get_ings_dict(ingredients_text):
        ings_dict = {}

        with suppress(IndexError):
            for ingredient in ingredients_text.split('\n'):
                split = ingredient.split('-', maxsplit=1)
                ings_dict[split[0].strip()] = split[1].strip()

        return ings_dict

    def save(self, commit=True):
        ings_text = self.cleaned_data.get('ingredients', None)
        ings_dict = self.get_ings_dict(ings_text)
        recipe = super(RecipeForm, self).save(commit=commit)
        self.create_ings(ings_dict, recipe.id)
        return recipe

    class Meta:
        model = Recipe
        fields = '__all__'
