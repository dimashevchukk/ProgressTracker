from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from tracker.models import MediaItem, Note


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name")


class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = [
            "title",
            "description",
            "cover",
            "total_progress",
            "release_date",
        ]


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "text"]
