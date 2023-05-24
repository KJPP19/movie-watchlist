from rest_framework import serializers
from rest_framework import permissions
from .models import *


"""Custom permissions"""
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
        fields = ['id', 'name']
    

class AvailablePlatformsMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailablePlatformsMovie
        fields = ['id', 'title']

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("title should have at least 3 characters")
        return value


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

        if StreamPlatform.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("Duplicate stream platform detected. '{}' already exist".format(validated_data['name']))

        for available_movie_data in available_movies_data:

            try:
                available_movie = AvailablePlatformsMovie.objects.filter(title=available_movie_data['title']).first()
                if available_movie not in available_movies:
                    available_movies.append(available_movie)
                else:
                    raise serializers.ValidationError("Duplicate available movies detected. '{}' already exist".format(available_movie_data['title']))
            except AvailablePlatformsMovie.DoesNotExist:
                available_movie = AvailablePlatformsMovie.objects.create(title=available_movie_data['title'])
                available_movies.append(available_movie)
        av_movie = StreamPlatform.objects.create(**validated_data)
        av_movie.available_movie.set(available_movies)
        return av_movie

    def update(self, instance, validated_data):
        available_movies_data = validated_data.pop('available_movie')
        available_movies = []

        if StreamPlatform.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("Duplicate stream platform detected. '{}' already exist".format(validated_data['name']))

        for available_movie_data in available_movies_data:

            try:
                available_movie = AvailablePlatformsMovie.objects.filter(title=available_movie_data['title']).first()
                if available_movie not in available_movies:
                    available_movies.append(available_movie)
                else: 
                    raise serializers.ValidationError("Duplicate available movies detected. '{}' already exist".format(available_movie_data['title']))
            except AvailablePlatformsMovie.DoesNotExist:
                available_movie = AvailablePlatformsMovie.objects.create(title=available_movie_data['title'])
                available_movies.append(available_movie)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        instance.available_movie.set(available_movies)
        return instance


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['id', 'title', 'runtime']


class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    stream_platform = StreamPlatformSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'synopsis', 'runtime', 'stream_platform']

    def validate_title(self, value):
        if len(value) < 3:
             raise serializers.ValidationError("title must be atleast 3 characters")
        return value

    def create(self, validated_data):

        movie_title = validated_data['title']
        genres_data = validated_data.pop('genre')
        stream_platforms_data = validated_data.pop('stream_platform')
        genres =[]
        streaming_platforms =[]
       
        if Movie.objects.filter(title=movie_title).exists():
            raise serializers.ValidationError("'{}' title already exist".format(movie_title))

        for genre_name in genres_data:
            try:
                genre = Genre.objects.get(name=genre_name['name'])
                if genre in genres:
                    raise serializers.ValidationError("'{}' genre already exist in this movie".format(genre_name['name']))
            except Genre.DoesNotExist:
                raise serializers.ValidationError("'{}' genre specified does not exist in the database".format(genre_name['name']))
            genres.append(genre)
        
        for platform_name in stream_platforms_data:
            try:
                streaming_platform = StreamPlatform.objects.get(name=platform_name['name'])
                if streaming_platform in streaming_platforms:
                    raise serializers.ValidationError("'{}' already exist for this movie".format(platform_name['name']))
                if not streaming_platform.available_movie.filter(title=movie_title).exists():
                    raise serializers.ValidationError("'{}' is not available to a specified stream platform".format(movie_title))
            except StreamPlatform.DoesNotExist:
                raise serializers.ValidationError("'{}' platform does not exist in the database".format(platform_name['name']))
            streaming_platforms.append(streaming_platform)

        movie = Movie.objects.create(**validated_data)
        movie.genre.set(genres)
        movie.stream_platform.set(streaming_platforms)
        return movie

    def update(self, instance, validated_data):

        movie_title = validated_data.get('title', instance.title)
        genres_data = validated_data.pop('genre')
        stream_platforms_data = validated_data.pop('stream_platform')
        genres =[]
        streaming_platforms =[]
       
        if Movie.objects.filter(title=movie_title).exists():
            raise serializers.ValidationError("'{}' title already exist".format(movie_title))

        for genre_name in genres_data:
            try:
                genre = Genre.objects.get(name=genre_name['name'])
                if genre in genres:
                    raise serializers.ValidationError("'{}' genre already exist in this movie".format(genre_name['name']))
            except Genre.DoesNotExist:
                raise serializers.ValidationError("'{}' genre specified does not exist in the database".format(genre_name['name']))
            genres.append(genre)
        
        for platform_name in stream_platforms_data:
            try:
                streaming_platform = StreamPlatform.objects.get(name=platform_name['name'])
                if streaming_platform in streaming_platforms:
                    raise serializers.ValidationError("'{}' already exist for this movie".format(platform_name['name']))
                if not streaming_platform.available_movie.filter(title=movie_title).exists():
                    raise serializers.ValidationError("'{}' is not available to a specified stream platform".format(movie_title))
            except StreamPlatform.DoesNotExist:
                raise serializers.ValidationError("'{}' platform does not exist in the database".format(platform_name['name']))
            streaming_platforms.append(streaming_platform)

        instance.title = movie_title
        instance.synopsis = validated_data.get('synopsis', instance.synopsis)
        instance.runtime = validated_data.get('runtime', instance.runtime)
        instance.save()
        instance.genre.set(genres)
        instance.stream_platform.set(streaming_platforms)
        return instance


class WatchListSerializer(serializers.ModelSerializer):
    movie = serializers.CharField()

    class Meta:
        model = WatchList
        fields = ['id', 'movie']

    def create(self, validated_data):
        movie_title = validated_data.get('movie')
        # print(validated_data)
        user = self.context['request'].user

        if WatchList.objects.filter(movie__title=movie_title, user=user).exists():
            raise serializers.ValidationError("'{}' already exist in your watchlist".format(movie_title))
        
        try:
            movie = Movie.objects.get(title=movie_title)
        except Movie.DoesNotExist:
            raise serializers.ValidationError("'{}' does not exist".format(movie_title))
        
        watchlist = WatchList.objects.create(user=user, movie=movie)
        return watchlist

    def update(self, instance, validated_data):
        movie_title = validated_data.get('movie')
        # print(validated_data)
        user = self.context['request'].user

        if WatchList.objects.filter(movie__title=movie_title, user=user).exists():
            raise serializers.ValidationError("'{}' already exist in your watchlist".format(movie_title))
        
        try:
            movie = Movie.objects.get(title=movie_title)
        except Movie.DoesNotExist:
            raise serializers.ValidationError("'{}' does not exist".format(movie_title))
        
        watchlist = WatchList.objects.create(user=user, movie=movie)

        instance.movie = movie
        instance.save()
        return instance


class ReviewListSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()
    reviewed_by = serializers.StringRelatedField()

    class Meta:
        model = MovieReview
        fields = ['id', 'movie', 'review', 'rating', 'reviewed_by']


class MovieReviewSerializer(serializers.ModelSerializer):
    movie = serializers.CharField()

    class Meta:
        model = MovieReview
        fields = ['id', 'movie', 'review', 'rating']
        
    def validate(self, data):
        if data['rating'] > 5 or data['rating'] < 1:
            raise serializers.ValidationError("rating must not exceed to 5 and not less than 1")
        if len(data['review']) < 10:
            raise serializers.ValidationError("review should have at least 10 characters")
        return data

    def create(self, validated_data):
        movie_title = validated_data.get('movie')
        reviewed_by = self.context['request'].user
        review = validated_data.get('review')
        rating = validated_data.get('rating')

        if MovieReview.objects.filter(movie__title=movie_title, reviewed_by=reviewed_by).exists():
            raise serializers.ValidationError("'{}' already exist in your reviews".format(movie_title))
        
        try:
            movie = Movie.objects.get(title=movie_title)
        except Movie.DoesNotExist:
            raise serializers.ValidationError("'{}' does not exist".format(movie_title))
        
        movie_review = MovieReview.objects.create(movie=movie, reviewed_by=reviewed_by, review=review, rating=rating)
        return movie_review
    
    def update(self, instance, validated_data):
        movie_title = validated_data.get('movie')
        reviewed_by = self.context['request'].user
        review = validated_data.get('review')
        rating = validated_data.get('rating')

        if MovieReview.objects.filter(movie__title=movie_title, reviewed_by=reviewed_by).exists():
            raise serializers.ValidationError("'{}' already exist in your reviews".format(movie_title))
        
        try:
            movie = Movie.objects.get(title=movie_title)
        except Movie.DoesNotExist:
            raise serializers.ValidationError("'{}' does not exist".format(movie_title))
        
        movie_review = MovieReview.objects.create(movie=movie, reviewed_by=reviewed_by, review=review, rating=rating)

        instance.movie = movie
        instance.review = review
        instance.rating = rating
        instance.save()
        return instance

