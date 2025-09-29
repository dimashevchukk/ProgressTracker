from django.urls import path

from tracker.views import (MediaCreateView, MediaDeleteView, MediaDetailView,
                           MediaListView, MediaUpdateView, NoteCreateView,
                           NoteDeleteView, NoteUpdateView, ProfileDetailView,
                           UserLibraryView, add_media_to_library,
                           remove_media_from_library)

app_name = "tracker"


urlpatterns = [
    path("", UserLibraryView.as_view(), name="index"),
    path("profiles/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profiles/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),
    path("items/<str:type>/", MediaListView.as_view(), name="media-list"),
    path("items/<str:type>/create/", MediaCreateView.as_view(), name="media-create"),
    path("items/<str:type>/<int:pk>/", MediaDetailView.as_view(), name="media-detail"),
    path(
        "items/<str:type>/<int:pk>/update/",
        MediaUpdateView.as_view(),
        name="media-update",
    ),
    path(
        "items/<str:type>/<int:pk>/delete/",
        MediaDeleteView.as_view(),
        name="media-delete",
    ),
    path("items/<str:type>/<int:pk>/add/", add_media_to_library, name="media-add"),
    path(
        "items/<str:type>/<int:pk>/remove/",
        remove_media_from_library,
        name="media-remove",
    ),
    path(
        "items/<int:user_media_id>/add_note/", NoteCreateView.as_view(), name="note-add"
    ),
    path("notes/<int:pk>/update/", NoteUpdateView.as_view(), name="note-update"),
    path("notes/<int:pk>/delete/", NoteDeleteView.as_view(), name="note-delete"),
]
