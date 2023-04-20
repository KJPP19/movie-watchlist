from django.contrib import admin
from .models import Genre, Movie, WatchList, MovieReview, StreamPlatform, AvailablePlatformsMovie


class MovieItemAdmin(admin.ModelAdmin):
    list_display = ["title", "synopsis", "created_at", "updated_at"]


class WatchListItemAdmin(admin.ModelAdmin):
    list_display = ["movie", "user"]


class StreamPlatformItemAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


class MovieReviewItemAdmin(admin.ModelAdmin):
    list_display = ["movie", "user", "added_at"]


admin.site.register(Genre)
admin.site.register(Movie, MovieItemAdmin)
admin.site.register(WatchList, WatchListItemAdmin)
admin.site.register(MovieReview, MovieReviewItemAdmin)
admin.site.register(StreamPlatform, StreamPlatformItemAdmin)
admin.site.register(AvailablePlatformsMovie)

