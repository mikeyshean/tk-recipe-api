from django.db import models


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name
