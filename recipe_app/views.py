from django.shortcuts import render


# Create your views here.
from recipe_app.models import Recipe, Author

def index_view(request):
    my_recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipes": my_recipes})


def recipe_details(request,recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    my_author = Author.objects.all()
    return render(request, "recipe_details.html",{"current_recipe":my_recipe, "authors":my_author})


def author_details(request,author_id):
    my_author = Author.objects.filter(id=author_id).first()
    my_recipes = Recipe.objects.filter(author= my_author)
    return render(request, "author_details.html",{"current_author":my_author, "recipes": my_recipes})
