from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Genre, StreamPlatform, AvailablePlatformsMovie, Movie, WatchList, MovieReview
from user.models import CustomUser


"""class MultipleRequest(TestCase):
    def test_200_request_get_all_movies(self):
         client = APIClient()
         for _ in range(200):
            response = client.get('/watchlist/v1/movies/')
            self.assertEqual(response.status_code, 200)"""


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
        self.assertEqual(Genre.objects.count(), 1)

    def test_create_genre(self):
        new_genre_data = {"name": "sci-fi"}
        previous_genre_count = Genre.objects.all().count()
        response = self.client.post(self.genre_url, data=new_genre_data)
        self.assertEqual(Genre.objects.all().count(), previous_genre_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print(response.data)
        self.assertEqual(response.data['name'], 'sci-fi')
        self.assertEqual(Genre.objects.count(), 2)

    def test_not_create_genre_if_blanked(self):
        blanked_data = {"name": ""}
        response = self.client.post(self.genre_url, data=blanked_data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error']['name'][0], 'This field may not be blank.')

    def test_create_duplicate_genre(self):
        genre_name = "comedy"
        Genre.objects.create(name=genre_name)
        duplicate_genre_data = {"name": genre_name}
        response = self.client.post(self.genre_url, data=duplicate_genre_data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['error'], 'genre duplicates detected')

    def test_get_one_genre(self):
        response = self.client.get(self.genre_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.genre_data['name'])

    def test_update_one_genre(self):
        update_genre_data = {"name": "romantic comedy"}
        response = self.client.put(self.genre_detail_url, data=update_genre_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'romantic comedy')

    def test_delete_one_genre(self):
        response = self.client.delete(self.genre_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Genre.objects.filter(pk=self.genre.pk).exists())


class StreamPlatformAPITest(APITestCase):

    def setUp(self):
        self.stream_platform_url = reverse('stream-platforms')
        self.stream_platform_data = {
            "name": "Netflix",
            "description": "popular streaming platform"
        }
        self.movie_data_1 = {"title": "Call"}
        self.movie_data_2 = {"title": "Hancock"}
        self.available_movie_1 = AvailablePlatformsMovie.objects.create(**self.movie_data_1)
        self.available_movie_2 = AvailablePlatformsMovie.objects.create(**self.movie_data_2)
        self.stream_platform = StreamPlatform.objects.create(**self.stream_platform_data)
        self.stream_platform.available_movie.set([self.available_movie_1, self.available_movie_2])
        self.stream_platform_detail_url = reverse('stream-platforms-detail', kwargs={'pk': self.stream_platform.pk})

    def test_get_all_stream_platforms(self):
        response = self.client.get(self.stream_platform_url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Netflix")
        self.assertEqual(response.data[0]["description"], "popular streaming platform")
        self.assertEqual(response.data[0]["available_movie"][0]["title"], "Call")
        self.assertEqual(response.data[0]["available_movie"][1]["title"], "Hancock")
        self.assertIsInstance(response.data, list)

    def test_create_stream_platform(self):
        new_movie_data = {"title": "Evil dead"}
        available_movie_3 = AvailablePlatformsMovie.objects.create(**new_movie_data)
        new_stream_platform_data = {
            "name": "HBO Max",
            "description": "another popular streaming platform",
            "available_movie": [{"title": self.available_movie_1.title}, {"title": self.available_movie_2.title},
                                {"title": available_movie_3.title}]
        }
        response = self.client.post(self.stream_platform_url, data=new_stream_platform_data, format="json")
        # print(response.data)
        # print(new_stream_platform_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'HBO Max')

    def test_available_movie_less_than_3_characters(self):
        new_movie_data = {"title": "Ev"}
        available_movie_3 = AvailablePlatformsMovie.objects.create(**new_movie_data)
        new_stream_platform_data = {
            "name": "HBO Max",
            "description": "another popular streaming platform",
            "available_movie": [{"title": self.available_movie_1.title}, {"title": self.available_movie_2.title},
                                {"title": available_movie_3.title}]
        }
        response = self.client.post(self.stream_platform_url, data=new_stream_platform_data, format="json")
        # print(response.data)
        # print(new_stream_platform_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_stream_platform(self):
        StreamPlatform.objects.create(name=self.stream_platform_data["name"])
        new_movie_data = {"title": "Evil dead"}
        available_movie_3 = AvailablePlatformsMovie.objects.create(**new_movie_data)
        new_stream_platform_data = {
            "name": self.stream_platform_data["name"],
            "description": "another popular streaming platform",
            "available_movie": [{"title": self.available_movie_1.title}, {"title": self.available_movie_2.title},
                                {"title": available_movie_3.title}]
        }
        response = self.client.post(self.stream_platform_url, data=new_stream_platform_data, format="json")
        # print(self.stream_platform_data["name"])
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_available_movies(self):
        new_stream_platform_data = {
            "name": "HBO Max",
            "description": "another popular streaming platform",
            "available_movie": [{"title": self.available_movie_1.title}, {"title": self.available_movie_1.title}]
        }
        response = self.client.post(self.stream_platform_url, data=new_stream_platform_data, format="json")
        # print(response.data)
        # print(new_stream_platform_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_one_stream_platform(self):
        response = self.client.get(self.stream_platform_detail_url, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Netflix")
        self.assertEqual(response.data["description"], "popular streaming platform")
        self.assertEqual(response.data["available_movie"][0]["title"], "Call")
        self.assertEqual(response.data["available_movie"][1]["title"], "Hancock")

    def test_update_one_stream_platform(self):
        update_stream_platform_data = {
            "name": "HULU",
            "description": "another great streaming platform",
            "available_movie": [{"title": self.available_movie_1.title}, {"title": self.available_movie_2.title}]
        }
        response = self.client.put(self.stream_platform_detail_url, data=update_stream_platform_data, format="json")
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'HULU')

    def test_update_available_movie(self):
        update_movie_data_1 = {"title": "Equalizer"}
        update_movie_data_2 = {"title": "Equalizer 2"}
        update_available_movie_1 = AvailablePlatformsMovie.objects.create(**update_movie_data_1)
        update_available_movie_2 = AvailablePlatformsMovie.objects.create(**update_movie_data_2)
        update_stream_platform_data = {
            "name": "HULU",
            "description": "another great streaming platform",
            "available_movie": [{"title": update_available_movie_1.title}, {"title": update_available_movie_2.title}]
        }
        response = self.client.put(self.stream_platform_detail_url, data=update_stream_platform_data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['available_movie'][0]['title'],  update_available_movie_1.title)

    def test_delete_one_stream_platform(self):
        response = self.client.delete(self.stream_platform_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'stream platform deleted')
        self.assertFalse(StreamPlatform.objects.filter(pk=self.stream_platform.pk).exists())


class MovieRetrieveAPITest(APITestCase):

    def setUp(self):
        self.movie_url = reverse('detailed-movie-list')
        self.movie_data = {
            "title": "call",
            "synopsis": "plot twist movie",
            "runtime": 147
        }
        self.genre_data_1 = {"name": "thriller"}
        self.genre_data_2 = {"name": "horror"}
        self.stream_platform_data_1 = {"name": "Netflix"}
        self.genre_1 = Genre.objects.create(**self.genre_data_1)
        self.genre_2 = Genre.objects.create(**self.genre_data_2)
        self.stream_platform_1 = StreamPlatform.objects.create(**self.stream_platform_data_1)
        self.movie = Movie.objects.create(**self.movie_data)
        self.movie.genre.set([self.genre_1, self.genre_2])
        self.movie.stream_platform.set([self.stream_platform_1])
        self.movie_detail_url = reverse('movie-detail', kwargs={'pk': self.movie.pk})

    def test_get_all_movies(self):
        response = self.client.get(self.movie_url, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]["title"], "call")
        self.assertEqual(response.data['results'][0]["synopsis"], "plot twist movie")
        self.assertEqual(response.data['results'][0]["runtime"], 147)
        self.assertEqual(response.data['results'][0]["genre"][0]["name"], "thriller")
        self.assertEqual(response.data['results'][0]["genre"][1]["name"], "horror")

    def test_get_one_movie(self):
        response = self.client.get(self.movie_detail_url, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "call")
        self.assertEqual(response.data["synopsis"], "plot twist movie")
        self.assertEqual(response.data["runtime"], 147)
        self.assertEqual(response.data["genre"][0]["name"], "thriller")
        self.assertEqual(response.data["genre"][1]["name"], "horror")


class MovieCreateAPITest(APITestCase):

    def setUp(self):
        self.movie_create_url = reverse('movie-create')
        self.stream_platform_data = {
            "name": "Netflix",
            "description": "popular streaming platform"
        }
        self.available_movie_data_1 = {"title": "Conjuring"}
        self.available_movie_data_2 = {"title": "Call"}
        self.available_movie_data_3 = {"title": "Murder Mystery"}
        self.stream_platform = StreamPlatform.objects.create(**self.stream_platform_data)
        self.available_movie_1 = AvailablePlatformsMovie.objects.create(**self.available_movie_data_1)
        self.available_movie_2 = AvailablePlatformsMovie.objects.create(**self.available_movie_data_2)
        self.available_movie_3 = AvailablePlatformsMovie.objects.create(**self.available_movie_data_3)
        self.stream_platform.available_movie.set([self.available_movie_1, self.available_movie_2,
                                                  self.available_movie_3])

        self.movie_data = {
            "title": "Call",
            "synopsis": "plot twist movie",
            "runtime": 147
        }
        self.genre_data_1 = {"name": "thriller"}
        self.genre_data_2 = {"name": "horror"}
        self.genre_data_3 = {"name": "comedy"}
        self.genre_1 = Genre.objects.create(**self.genre_data_1)
        self.genre_2 = Genre.objects.create(**self.genre_data_2)
        self.genre_3 = Genre.objects.create(**self.genre_data_3)
        self.movie = Movie.objects.create(**self.movie_data)
        self.movie.genre.set([self.genre_1, self.genre_2, self.genre_3])
        self.movie.stream_platform.set([self.stream_platform])

    def test_create_valid_movie(self):
        new_movie_data = {
            "title": self.available_movie_1.title,
            "synopsis": "plot twist movie",
            "runtime": 147,
            "genre": [
                {"name": self.genre_1.name},
                {"name": self.genre_2.name}
            ],
            "stream_platform": [
                {"name": self.stream_platform.name}
            ]
        }
        response = self.client.post(self.movie_create_url, data=new_movie_data, format="json")
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print(response.data)
        self.assertEqual(response.data['title'], 'Conjuring')
        self.assertEqual(response.data['genre'][0]['name'], 'thriller')
        self.assertEqual(response.data['genre'][1]['name'], 'horror')
        self.assertEqual(response.data['stream_platform'][0]['name'], 'Netflix')
        self.assertEqual(Movie.objects.count(), 2)

    def test_create_invalid_movie(self):
        new_movie_data = {
            "title": "Hangover",
            "synopsis": "The Hangover is a trilogy of American "
                        "comedy films created by Jon Lucas and Scott Moore, and directed by Todd Phillips. ",
            "runtime": 130,
            "genre": [
                {"name": self.genre_3.name}
            ],
            "stream_platform": [
                {"name": self.stream_platform.name}
            ]
        }
        response = self.client.post(self.movie_create_url, data=new_movie_data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_movie_invalid_stream_platform(self):
        new_movie_data = {
            "title": self.available_movie_3.title,
            "synopsis": "plot twist, twist and turns",
            "runtime": 120,
            "genre": [
                {"name": self.genre_3.name}
            ],
            "stream_platform": [
                {"name": "HBO max"}
            ]
        }
        response = self.client.post(self.movie_create_url, data=new_movie_data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_movie_invalid_genre(self):
        new_movie_data = {
            "title": self.available_movie_3.title,
            "synopsis": "plot twist, twist and turns",
            "runtime": 120,
            "genre": [
                {"name": "documentary"}
            ],
            "stream_platform": [
                {"name": self.stream_platform.name}
            ]
        }
        response = self.client.post(self.movie_create_url, data=new_movie_data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_movie_less_than_3_characters(self):
        new_movie_data = {
            "title": "ui",
            "synopsis": "sample plot of the movie",
            "runtime": 130,
            "genre": [
                {"name": self.genre_1.name}
            ],
            "stream_platform": [
                {"name": self.stream_platform.name}
            ]
        }
        response = self.client.post(self.movie_create_url, data=new_movie_data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error']['title'][0], 'title must be atleast 3 characters')


class WatchListApiTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@sample.com', password='123456789',
                                                   role='watcher')
        self.movie = Movie.objects.create(title='Conjuring', runtime='147')
        self.watchlist = WatchList.objects.create(user=self.user, movie=self.movie)
        self.watchlist_url = reverse('watchlist', kwargs={'user_id': self.user.id})
    
    def test_get_user_own_watchlist(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.watchlist_url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_user_role_is_not_watcher(self):
        self.new_user = CustomUser.objects.create_user(email='testuser2@sample.com', password='123456789',
                                                       role='visitor')
        self.client.force_authenticate(user=self.new_user)
        self.watchlist = WatchList.objects.create(user=self.new_user, movie=self.movie)
        response = self.client.get(self.watchlist_url)
        # print(response.data)
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'user is not watcher')

    def test_get_other_user_watchlist(self):
        self.new_user = CustomUser.objects.create_user(email='testuser3@sample.com', password='123456789',
                                                   role='watcher')
        self.client.force_authenticate(user=self.new_user)
        response = self.client.get(self.watchlist_url)
        # print(response.data, response.status_code)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "you are not authorized to access this watchlist")
    

class WatchListCreateApiTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@sample.com', password='123456789',
                                                   role='watcher')
        self.movie_data_1 = Movie.objects.create(title='Conjuring', runtime='147') # available movie for adding to user's watchlist
        self.movie_data_2 = Movie.objects.create(title='John Wick', runtime='125') # available movie for adding to user's watchlist
        self.watchlist = WatchList.objects.create(user=self.user, movie=self.movie_data_1)
        self.add_to_watchlist_url = reverse('watchlist-add', kwargs={'user_id': self.user.id})
    
    def test_post_valid_movie_to_watchlist(self):
        new_watchlist_data = {
            "movie": "John Wick"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.add_to_watchlist_url, data=new_watchlist_data, format="json")
        # print(response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['movie'], 'John Wick')
        self.assertEqual(WatchList.objects.count(), 2)
    
    def test_post_invalid_movie_to_watchlist(self):
        invalid_watchlist_data = {
            "movie": "Sinister"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.add_to_watchlist_url, data=invalid_watchlist_data, format="json")
        # print(response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['error'][0]), "'{}' does not exist".format(invalid_watchlist_data['movie']))
        self.assertEqual(WatchList.objects.count(), 1)


class MovieReviewListApiTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@sample.com', password='123456789',
                                                   role='reviewer')
        self.movie_data_1 = Movie.objects.create(title='Conjuring', runtime='147') # available movie to review
        self.movie_data_2 = Movie.objects.create(title='John Wick', runtime='125') # available movie to review
        self.movie_review = MovieReview.objects.create(reviewed_by=self.user, 
                                                       movie=self.movie_data_1, review="real life story horror movie", rating=5)
        """since creating a movie review needs users to be authenticated and viewing the movie review list is public,
            separate URL for adding movie review and viewing movie review list"""
        self.add_movie_review_url = reverse('add-movie-review', kwargs={'user_id': self.user.id})
        self.movie_review_list_url = reverse('movie-reviews-list')

    def test_get_movie_reviews(self):
        response = self.client.get(self.movie_review_list_url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['movie'], 'Conjuring')
        self.assertEqual(response.data['results'][0]['reviewed_by'], 'testuser@sample.com')
        self.assertEqual(response.data['count'], 1)

    def test_add_valid_movie_review(self):
        self.client.force_authenticate(user=self.user)
        new_review_data = {
            "movie": "John Wick",
            "review": "full of action and good story",
            "rating": 4
        }
        response = self.client.post(self.add_movie_review_url, data=new_review_data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['movie'], 'John Wick')
        self.assertEqual(MovieReview.objects.count(), 2)

    def test_add_invalid_movie_review(self):
        self.client.force_authenticate(user=self.user)
        """John Wick 2 was not in the database, available movies to review are Conjuring and John Wick"""
        invalid_review_data = {
            "movie": "John Wick 2",
            "review": "full of action and good story",
            "rating": 5
        }
        response = self.client.post(self.add_movie_review_url, data=invalid_review_data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['error'][0]), "'{}' does not exist".format(invalid_review_data['movie']))
        self.assertEqual(MovieReview.objects.count(), 1)