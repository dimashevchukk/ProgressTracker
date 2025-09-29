from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from tracker.forms import CustomUserCreationForm, NoteForm, MediaItemForm
from tracker.models import MediaItem, Note, Profile, UserMedia

User = get_user_model()


class UserRegistrationView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("tracker:index")


class UserLibraryView(LoginRequiredMixin, generic.ListView):
    model = UserMedia
    template_name = "tracker/index.html"
    context_object_name = "user_media_list"

    def get_queryset(self):
        return UserMedia.objects.select_related("item").filter(user=self.request.user)


class ProfileDetailView(generic.DetailView):
    model = Profile
    context_object_name = "profile"

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")

        if pk:
            return Profile.objects.get(pk=pk)

        if self.request.user.is_authenticated:
            return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            user_media = user.media.select_related("item")
            context["user_media"] = user_media
            context["media_titles"] = [um.item.title for um in user_media]
        else:
            context["user_media"] = []
            context["media_titles"] = []

        return context


class MediaCreateView(generic.CreateView):
    model = MediaItem
    form_class = MediaItemForm

    def form_valid(self, form):
        form.instance.type = self.kwargs["type"]
        return super().form_valid(form)

    def get_success_url(self):
        return redirect(
            "tracker:media-list",
            type=self.object.type,
        ).url


class MediaListView(generic.ListView):
    model = MediaItem

    def get_queryset(self):
        media_type = self.kwargs.get("type")
        return MediaItem.objects.filter(type=media_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["media_type"] = self.kwargs.get("type")

        if self.request.user.is_authenticated:
            context["user_media_ids"] = self.request.user.media.values_list(
                "item_id", flat=True
            )

        return context


class MediaDetailView(generic.DetailView):
    model = MediaItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_media = UserMedia.objects.filter(
                user=self.request.user, item=self.object
            ).first()
            context["user_media"] = user_media

            if user_media:
                context["notes"] = user_media.notes.order_by("-created_at")

        return context


class MediaDeleteView(generic.DeleteView):
    model = MediaItem

    def get(self, request, pk, *args, **kwargs):
        media = get_object_or_404(MediaItem, pk=pk)
        if request.user.is_staff:
            media.delete()
        return redirect("tracker:media-list", type=media.type)


@login_required
def add_media_to_library(request: HttpRequest, type: str, pk: int) -> HttpResponse:
    media_item = get_object_or_404(MediaItem, pk=pk)
    UserMedia.objects.create(user=request.user, item=media_item)
    return redirect("tracker:media-detail", type=media_item.type, pk=pk)


@login_required
def remove_media_from_library(request: HttpRequest, type: str, pk: int) -> HttpResponse:
    user_media = get_object_or_404(
        UserMedia,
        user_id=request.user.id,
        item_id=pk,
    )
    user_media.delete()
    return redirect("tracker:media-list", type=user_media.item.type)


class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Note
    form_class = NoteForm

    def form_valid(self, form):
        user_media_id = self.kwargs.get("user_media_id")
        user_media = get_object_or_404(UserMedia, id=user_media_id)
        form.instance.user_media = user_media
        return super().form_valid(form)

    def get_success_url(self):
        return redirect(
            "tracker:media-detail",
            type=self.object.user_media.item.type,
            pk=self.object.user_media.item.pk,
        ).url


class NoteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Note
    form_class = NoteForm

    def form_valid(self, form):
        user_media_id = self.kwargs.get("user_media_id")
        user_media = get_object_or_404(UserMedia, id=user_media_id)
        form.instance.user_media = user_media
        return super().form_valid(form)

    def get_success_url(self):
        return redirect(
            "tracker:media-detail",
            type=self.object.user_media.item.type,
            pk=self.object.user_media.item.pk,
        ).url


class NoteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Note

    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        if note.user_media.user == request.user:
            note.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))
