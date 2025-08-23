from django.urls import path

from tracker.views import index


urlpatterns = [
    path("", index, name="index"),
]
