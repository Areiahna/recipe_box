from django.shortcuts import render, HttpResponseRedirect, reverse


# Create your views here.
from recipe_app.models import Recipe, Author
from recipe_app.forms import AddAuthorForm, AddRecipeForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required


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


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                author=request.user.author,
                description=data.get('description'),
                instructions=data.get('instructions'),
                time=data.get('time'),
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {"form": form})

def recipe_edit(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recipe.title = data["title"]
            recipe.description = data["description"]
            recipe.author = data["author"]
            recipe.instructions = data["instructions"]
            recipe.time = data["time"]
            recipe.save()
        return HttpResponseRedirect(reverse("recipe_details", args=[recipe.id]))
    data = {
        "title": recipe.title,
        "description": recipe.description,
        "time": recipe.time,
        "author": recipe.author,
        "instructions": recipe.instructions,
    }
    form = AddRecipeForm(initial=data)
    return render(request, "generic_form.html", {"form": form})


@login_required
@staff_member_required
def add_author(request):
    # Worked with Peter
    # https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/#the-save-method
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get(
                "username"), password=data.get("password"))
            new_author = form.save(commit=False)
            new_author.user = new_user
            new_author.save()
            return HttpResponseRedirect(reverse("homepage"))

    form = AddAuthorForm
    return render(request, "generic_form.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))
                # return HttpResponseRedirect(reverse("homepage"))

    form = LoginForm
    return render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))

def add_favorite(request, fav_id):
    favorited = Recipe.objects.filter(id=fav_id).first()
    logged_in_user = request.user
    breakpoint()
    logged_in_user.author.favorites.add(favorited)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
