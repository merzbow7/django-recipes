# Create your views here.
from django.http import QueryDict
from django.views.generic import ListView, DetailView

from .models import Recipe


class AllRecipesView(ListView):

    def get_queryset(self):
        return Recipe.objects.all()


class FilterRecipesView(ListView):

    def get_queryset(self):
        params: QueryDict = self.request.GET
        choose = params.get('choose')
        query = params.get('query')
        if choose == "recipe":
            query_set = Recipe.objects.filter(
                title__icontains=query
            )
        else:
            query_set = Recipe.objects.filter(
                recipeingredient__name__name__icontains=query
            )
        return query_set

    def get_context_data(self, **kwargs):
        context = super(FilterRecipesView, self).get_context_data(**kwargs)
        if self.request.GET.get('choose') == 'ingredient':
            context['ingredient_select'] = 'selected'
        else:
            context['recipe_select'] = 'selected'
        context['query'] = self.request.GET.get('query')
        return context


class RecipeView(DetailView):

    def get_queryset(self):
        return Recipe.objects.filter(slug__exact=self.kwargs.get("slug"))
