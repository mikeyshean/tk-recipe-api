from django.test import TestCase

from core import models


class ModelTests(TestCase):

    def test_ingredient_str(self):
        """Test the ingredient stringn representation"""
        ingredient = models.Ingredient.objects.create(
            name="Cucumber"
        )

        self.assertEqual(str(ingredient), ingredient.name)
