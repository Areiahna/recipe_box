from django.shortcuts import render, HttpResponseRedirect, reverse


# Create your views here.
from recipe_app.models import Recipe, Author
from recipe_app.forms import AddAuthorForm, AddRecipeForm


def index_view(request):
    my_recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipes": my_recipes})


def recipe_details(request, recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_details.html", {"current_recipe": my_recipe})


def author_details(request, author_id):
    my_author = Author.objects.filter(id=author_id).first()
    my_recipes = Recipe.objects.filter(author=my_author)
    return render(request, "author_details.html", {"current_author": my_author, "recipes": my_recipes})


def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                author=data.get('author'),
                description=data.get('description'),
                instructions=data.get('instructions'),
                time=data.get('time')
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {"form": form})


def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse("homepage"))

    form = AddAuthorForm
    return render(request, "generic_form.html", {"form": form})
