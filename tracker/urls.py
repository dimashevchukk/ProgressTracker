from django.urls import path

from tracker.views import (
    index,
    ProfileDetailView,
    MediaListView,
    MediaDetailView,
    add_media_to_library, add_note,
)

app_name = "tracker"


urlpatterns = [
    path("", index, name="index"),
    path("profile/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),

    path("media/<str:type>/", MediaListView.as_view(), name="media-list"),
    path("media/<str:type>/<int:pk>/", MediaDetailView.as_view(), name="media-detail"),
    path("media/<str:type>/<int:pk>/add/", add_media_to_library, name="media-add"),
    path("media/<int:user_media_id>/add_note/", add_note, name="note-add"),
]
