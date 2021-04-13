from rest_framework import viewsets, mixins

from core.models import Recipe, Ingredient

from recipe import serializers


class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage recipes in the database"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
