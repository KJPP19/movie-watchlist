from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Genre


class GenreAPITest(APITestCase):

    def setUp(self):
        self.genre_url = reverse('genre-list')
        self.genre_data = {"name": "documentary"}
        self.genre = Genre.objects.create(**self.genre_data)
        self.genre_detail_url = reverse('genre-detail', kwargs={'pk': self.genre.pk})  # for testing genre detail

    def test_get_all_genre(self):
        response = self.client.get(self.genre_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data[0]["name"], "documentary")

    def test_create_genre(self):
        new_genre_data = {"name": "sci-fi"}
        previous_genre_count = Genre.objects.all().count()
        response = self.client.post(self.genre_url, data=new_genre_data)
        self.assertEqual(Genre.objects.all().count(), previous_genre_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print(response.data)
        self.assertEqual(response.data['message'], 'genre created')

    def test_not_create_genre_if_blanked(self):
        blanked_data = {"name": ""}
        response = self.client.post(self.genre_url, data=blanked_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_genre(self):
        genre_name = "comedy"
        Genre.objects.create(name=genre_name)
        duplicate_genre_data = {"name": genre_name}
        response = self.client.post(self.genre_url, data=duplicate_genre_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'genre already exist')

    def test_get_one_genre(self):
        response = self.client.get(self.genre_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.genre_data['name'])

    def test_update_one_genre(self):
        update_genre_data = {"name": "romantic comedy"}
        response = self.client.put(self.genre_detail_url, data=update_genre_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'genre updated')

    def test_delete_one_genre(self):
        response = self.client.delete(self.genre_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Genre.objects.filter(pk=self.genre.pk).exists())








