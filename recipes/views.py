"""Views for recipe app."""
from django.views.generic import DetailView, ListView

from recipes.models import Recipe


class AllRecipesView(ListView):
    """List of all Recipes."""

    def get_queryset(self):
        """Return all recipes."""
        return Recipe.objects.all()


class FilterRecipesView(ListView):
    """Filter Recipes title and ingredients."""

    @property
    def get_params(self) -> tuple[str, str]:
        """Get filter choose and query string."""
        try:
            choose = self.request.GET.get('choose')
        except (ValueError, TypeError):
            choose = None

        try:
            query = self.request.GET.get('query')
        except (ValueError, TypeError):
            query = None

        return choose, query

    def get_queryset(self, **kwargs):
        """Get queryset for filter view."""
        choose, query = self.get_params

        if choose == 'recipe':
            query_set = Recipe.objects.filter(
                title__icontains=query,
            )
        else:
            query_set = Recipe.objects.filter(
                recipeingredient__name__name__icontains=query,
            )
        return query_set

    def get_context_data(self, **kwargs):
        """Get context for filtering."""
        context = super().get_context_data(**kwargs)

        choose, query = self.get_params

        if choose == 'ingredient':
            context['ingredient_select'] = 'selected'
        else:
            context['recipe_select'] = 'selected'
        context['query'] = query

        return context


class RecipeView(DetailView):
    """Recipe view."""

    def get_queryset(self):
        """Get queryset for Recipe detail vie."""
        return Recipe.objects.filter(slug__exact=self.kwargs.get('slug'))
