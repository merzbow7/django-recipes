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
        btn = params.get('btn')
        query_set = Recipe.objects.filter(title__icontains=query)
        print(query_set)
        return query_set


class RecipeView(DetailView):

    def get_queryset(self):
        return Recipe.objects.filter(slug__exact=self.kwargs.get("slug"))
