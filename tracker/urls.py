from django.urls import path

from tracker.views import (
    index,
    ProfileDetailView,
    MediaListView,
    MediaDetailView,
)

app_name = "tracker"


urlpatterns = [
    path("", index, name="index"),
    path("profile/", ProfileDetailView.as_view(), name="profile-detail"),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile-detail"),

    path("media/<str:type>/", MediaListView.as_view(), name="media-list"),
    path("media/<str:type>/<int:pk>/", MediaDetailView.as_view(), name="media-detail")
]
