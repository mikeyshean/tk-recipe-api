from django.test import TestCase

from core import models


class ModelTests(TestCase):

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        recipe = models.Recipe.objects.create(
            name="Pizza",
            description="Cheesy Goodness",
        )
        ingredient = models.Ingredient.objects.create(
            name="Cucumber",
            recipe=recipe
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            name="Pizza",
            description="Cheesy Goodness",
        )
        self.assertEqual(str(recipe), recipe.name)
