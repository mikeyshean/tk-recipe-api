from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(name='Default Name', description='Default Description'):
    """Create sample recipe"""
    return Recipe.objects.create(name=name, description=description)


def detail_url(recipe_id):
    """Returns recipe detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


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

    def test_create_recipe_with_invalid_ingredients(self):
        """Test creating a recipe with blank ingredient name"""
        payload = {
            'name': 'Cheeseburger',
            'description': 'Yummy',
            'ingredients': [
                {'name': 'Meat'},
                {'name': 'Bun'},
                {'name': ''}
            ]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recipe_invalid_name(self):
        """Test creating recipe without name"""
        payload = {'name': ''}
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_recipes(self):
        """Test retrieving recipe api data"""
        sample_recipe(name='Cheeseburger')
        sample_recipe(name='Soup')

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_recipe_new_ingredients_successful(self):
        """Test updating recipe with list of ingredients"""
        recipe = sample_recipe(name='Cheeseburger', description='Yummy')
        payload = {
            'id': recipe.id,
            'name': recipe.name,
            'description': recipe.description,
            'ingredients': [
                {'name': 'Cheese'}, {'name': 'Bun'}, {'name': 'Meat'}
            ]
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload, format='json')
        recipe.refresh_from_db()
        serializer = RecipeSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_update_recipe_all_fields_successful(self):
        """Test updating recipe with replacement ingredients"""

        """Create initial recipe with ingredients first"""
        recipe = sample_recipe(name='Cheeseburger', description='Yummy')
        payload = {
            'id': recipe.id,
            'name': recipe.name,
            'description': recipe.description,
            'ingredients': [
                {'name': 'Cheese'}, {'name': 'Bun'}, {'name': 'Meat'}
            ]
        }
        url = detail_url(recipe.id)
        self.client.put(url, payload, format='json')

        """Update recipe with new data"""
        payload2 = {
            'id': recipe.id,
            'name': 'Ice Cream',
            'description': 'Cold',
            'ingredients': [{'name': 'Vanilla'}]
        }

        res2 = self.client.put(url, payload2, format='json')
        recipe.refresh_from_db()

        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.name, payload2['name'])
        self.assertEqual(recipe.description, payload2['description'])
        self.assertEqual(
            len(recipe.ingredients.all()),
            len(payload2['ingredients'])
        )

        serializer = RecipeSerializer(recipe)
        self.assertEqual(serializer.data, res2.data)

    def test_update_invalid_recipe(self):
        """Test updating invalid recipe"""
        url = detail_url(-1)
        res = self.client.put(url, {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_recipe_successful(self):
        """Test deleting recipe also delete ingredients"""

        """Create initial recipe with ingredients first"""
        recipe = sample_recipe(name='Cheeseburger', description='Yummy')
        payload = {
            'id': recipe.id,
            'name': recipe.name,
            'description': recipe.description,
            'ingredients': [
                {'name': 'Cheese'}, {'name': 'Bun'}, {'name': 'Meat'}
            ]
        }
        url = detail_url(recipe.id)
        self.client.put(url, payload, format='json')

        query_set1 = Ingredient.objects.filter(recipe=recipe)
        self.assertTrue(query_set1.exists())

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        query_set2 = Ingredient.objects.filter(recipe=recipe)
        self.assertFalse(query_set2.exists())

    def test_delete_recipe_invalid(self):
        """Test deleting invalid recipe fails"""
        url = detail_url(-1)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_recipe_filter_with_substring(self):
        """Test retrieving recipes with substring filter"""
        recipe1 = sample_recipe(name='Beef Patty')
        recipe2 = sample_recipe(name='Taco with beef')
        recipe3 = sample_recipe(name='Fish and chips')

        res = self.client.get(RECIPES_URL, {'name': 'beef'})

        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        serializer3 = RecipeSerializer(recipe3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
