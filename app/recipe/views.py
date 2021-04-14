from rest_framework import viewsets, mixins

from core.models import Recipe, Ingredient

from recipe import serializers


class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage recipes in the database"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_serializer_class(self):
        """Return serializer class"""
        return self.serializer_class

    def perform_create(self, serializer):
        """Create new ingredient"""
        serializer.save()


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

    def get_serializer_class(self):
        """Return serializer class"""
        return self.serializer_class

    def perform_create(self, serializer):
        """Create new recipe"""
        serializer.save()
