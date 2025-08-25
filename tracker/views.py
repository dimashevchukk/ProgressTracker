from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from tracker.models import Profile, MediaItem
from tracker.forms import CustomUserCreationForm


User = get_user_model()


class UserRegistrationView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("tracker:index")


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "tracker/index.html")


class ProfileDetailView(generic.DetailView):
    model = Profile
    context_object_name = "profile"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")

        if pk:
            return Profile.objects.get(pk=pk)

        if self.request.user.is_authenticated:
            return self.request.user

    def get_context_data(self, **kwargs):   # need to add mediaitems later
        context = super().get_context_data(**kwargs)
        return context


class MediaListView(generic.ListView):
    model = MediaItem

    def get_queryset(self):
        media_type = self.kwargs.get("type")
        return MediaItem.objects.filter(type=media_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_type"] = self.kwargs.get("type")
        return context


class MediaDetailView(generic.DetailView):
    model = MediaItem
