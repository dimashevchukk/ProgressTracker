from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from tracker.models import Profile, MediaItem, UserMedia, Note
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_media = UserMedia.objects.filter(
                user=self.request.user,
                item=self.object
            ).first()
            context["user_media"] = user_media

            if user_media:
                context["notes"] = user_media.notes.all()

        return context


@login_required
def add_media_to_library(request: HttpRequest, type: str, pk: int) -> HttpResponse:
    media_item = get_object_or_404(MediaItem, pk=pk)
    UserMedia.objects.create(
        user=request.user,
        item=media_item
    )
    return redirect("tracker:media-detail", type=media_item.type, pk=pk)


@login_required
def add_note(request, user_media_id):
    user_media = get_object_or_404(UserMedia, id=user_media_id)
    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Note.objects.create(user_media=user_media, text=text)

    return redirect("tracker:media-detail", type=user_media.item.type, pk=user_media.item.pk)
