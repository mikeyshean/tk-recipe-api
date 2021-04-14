from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(name='Default Name', description='Default Description'):
    return Recipe.objects.create(name=name, description=description)


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_create_recipe_without_ingredients_successful(self):
        """Test creating a recipe"""
        payload = {
            'name': 'Cheeseburger',
            'description': 'Yummy',
            'ingredients': []
        }

        res = self.client.post(RECIPES_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])
        self.assertEqual(res.data['description'], payload['description'])
        self.assertEqual(len(res.data['ingredients']), 0)

    def test_create_recipe_with_ingredients_successful(self):
        """Test creating a recipe"""
        payload = {
            'name': 'Cheeseburger',
            'description': 'Yummy',
            'ingredients': [
                {'name': 'Meat'},
                {'name': 'Bun'},
                {'name': 'Cheese'}
            ]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload_ingredients = sorted(payload['ingredients'],
                                     key=lambda ingredient: ingredient['name'])
        recipe_ingredients = sorted(res.data['ingredients'],
                                    key=lambda ingredient: ingredient['name'])
        self.assertEqual(payload_ingredients, recipe_ingredients)
        self.assertEqual(res.data['name'], payload['name'])
        self.assertEqual(res.data['description'], payload['description'])

    def test_retrieve_recipes(self):
        """Test retrieving recipe api data"""
        sample_recipe(name='Cheeseburger')
        sample_recipe(name='Soup')

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
