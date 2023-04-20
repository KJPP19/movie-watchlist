from rest_framework import serializers
from rest_framework import permissions
from .models import *


class IsWatcher(permissions.BasePermission):
    message = 'user is not watcher'

    def has_permission(self, request, view):
        return request.user.role == 'watcher'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'watcher'


class IsReviewer(permissions.BasePermission):
    message = 'user is not a reviewer'

    def has_permission(self, request, view):
        return request.user.role == 'reviewer'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'reviewer'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['name']


class AvailablePlatformsMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailablePlatformsMovie
        fields = ['id', 'title']


class StreamPlatformSerializer(serializers.ModelSerializer):
    available_movie = AvailablePlatformsMovieSerializer(many=True, required=False)

    class Meta:
        model = StreamPlatform
        fields = ['id', 'name', 'description', 'available_movie']
        extra_kwargs = {
            'description': {'required': False},
            'available_movie': {'required': False},
        }

    def create(self, validated_data):
        available_movies_data = validated_data.pop('available_movie')
        available_movies = []
        for available_movie_data in available_movies_data:

            try:
                available_movie = AvailablePlatformsMovie.objects.get(title=available_movie_data['title'])
                if available_movie in available_movies:
                    raise serializers.ValidationError('movie was already added to this platform')
            except AvailablePlatformsMovie.DoesNotExist:
                available_movie = AvailablePlatformsMovie.objects.create(title=available_movie_data['title'])
            available_movies.append(available_movie)
        av_movie = StreamPlatform.objects.create(**validated_data)
        av_movie.available_movie.set(available_movies)
        return av_movie

    def update(self, instance, validated_data):
        available_movies_data = validated_data.pop('available_movie')
        available_movies = []
        for available_movie_data in available_movies_data:

            try:
                available_movie = AvailablePlatformsMovie.objects.get(title=available_movie_data['title'])
                if available_movie in available_movies:
                    raise serializers.ValidationError('movie was already added to this platform')
            except AvailablePlatformsMovie.DoesNotExist:
                available_movie = AvailablePlatformsMovie.objects.create(title=available_movie_data['title'])
            available_movies.append(available_movie)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        instance.available_movie.set(available_movies)
        return instance


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    stream_platform = StreamPlatformSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'synopsis', 'runtime', 'stream_platform']

    def validate(self, data):
        if len(data['title']) < 3:
            raise serializers.ValidationError("title should have at least 3 letters")
        return data

    def create(self, validated_data):

        title = validated_data['title']
        stream_platforms_data = validated_data['stream_platform']
        for platform_data in stream_platforms_data:

            try:
                stream_platform = StreamPlatform.objects.get(name=platform_data['name'])
            except StreamPlatform.DoesNotExist:
                raise serializers.ValidationError("stream platform does not exist")
            if not stream_platform.available_movie.filter(title=title).exists():
                raise serializers.ValidationError("this movie does not exist on the specified streaming platform")

        genres_data = validated_data.pop('genre')
        genres = []
        for genre_data in genres_data:

            try:
                genre = Genre.objects.get(name=genre_data['name'])
            except Genre.DoesNotExist:
                raise serializers.ValidationError("invalid Genre")
            genres.append(genre)

        stream_platforms_data = validated_data.pop('stream_platform')
        stream_platforms = []
        for platform_data in stream_platforms_data:

            try:
                stream_platform = StreamPlatform.objects.get(name=platform_data['name'])
            except StreamPlatform.DoesNotExist:
                raise serializers.ValidationError("stream platform does not exist")
            stream_platforms.append(stream_platform)

        movie = Movie.objects.create(**validated_data)
        movie.genre.set(genres)
        movie.stream_platform.set(stream_platforms)
        return movie

    def update(self, instance, validated_data):

        title = validated_data.get('title', instance.title)
        stream_platforms_data = validated_data.get('stream_platform', instance.stream_platform.all())
        for platform_data in stream_platforms_data:

            try:
                stream_platform = StreamPlatform.objects.get(name=platform_data['name'])
            except StreamPlatform.DoesNotExist:
                raise serializers.ValidationError("stream platform does not exist")
            if not stream_platform.available_movie.filter(title=title).exists():
                raise serializers.ValidationError("this movie is not available on this platform you specified")

        genres_data = validated_data.pop('genre')
        genres = []
        for genre_data in genres_data:

            try:
                genre = Genre.objects.get(name=genre_data['name'])
            except Genre.DoesNotExist:
                raise serializers.ValidationError("invalid Genre")
            genres.append(genre)

        stream_platforms_data = validated_data.pop('stream_platform')
        stream_platforms = []
        for platform_data in stream_platforms_data:

            try:
                stream_platform = StreamPlatform.objects.get(name=platform_data['name'])
            except StreamPlatform.DoesNotExist:
                raise serializers.ValidationError("stream platform does not exist")
            stream_platforms.append(stream_platform)

        instance.title = title
        instance.synopsis = validated_data.get('synopsis', instance.synopsis)
        instance.runtime = validated_data.get('runtime', instance.runtime)
        instance.save()
        instance.genre.set(genres)
        instance.stream_platform.set(stream_platforms)
        return instance


class WatchListSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()

    class Meta:
        model = WatchList
        fields = ['id', 'movie']


class MovieReviewSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()

    class Meta:
        model = MovieReview
        fields = ['id', 'movie', 'review']


