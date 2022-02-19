from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from recipes import views

urlpatterns = [
    path('', views.AllRecipesView.as_view(), name='recipes_index'),
    path('filter/', views.FilterRecipesView.as_view(), name='recipes_filter'),
    path('recipes/<slug:slug>', views.RecipeView.as_view(), name='recipe_url'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)