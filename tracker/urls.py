from django.urls import path

from tracker.views import (
    index,
    ProfileDetailView,
    GameListView,
    BookListView,
    MovieListView,
)

app_name = "tracker"


urlpatterns = [
    path("", index, name="index"),
    path("profile/", ProfileDetailView.as_view(), name="profile-detail"),

    path("games/", GameListView.as_view(), name="game-list"),
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("books/", BookListView.as_view(), name="book-list"),
]
