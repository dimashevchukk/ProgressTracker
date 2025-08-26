from django.urls import path

from tracker.views import (
    UserLibraryView,
    ProfileDetailView,
    MediaListView,
    MediaDetailView,
    add_media_to_library,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
)

app_name = "tracker"


urlpatterns = [
    path("", UserLibraryView.as_view(), name="index"),
    path("profile/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),

    path("media/<str:type>/", MediaListView.as_view(), name="media-list"),
    path("media/<str:type>/<int:pk>/", MediaDetailView.as_view(), name="media-detail"),
    path("media/<str:type>/<int:pk>/add/", add_media_to_library, name="media-add"),
    path("media/<int:user_media_id>/add_note/", NoteCreateView.as_view(), name="note-add"),
    path("notes/<int:pk>/update/", NoteUpdateView.as_view(), name="note-update"),
    path("notes/<int:pk>/delete/", NoteDeleteView.as_view(), name="note-delete"),
]
