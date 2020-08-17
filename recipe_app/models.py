from django.db import models
from django.contrib.auth.models import User
#


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=60)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    instructions = models.TextField()
    time = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} - {self.author.name}"
