from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(
        upload_to="images/avatars/",
        blank=True, null=True,
        default="images/avatars/default_avatar.jpg"
    )
    bio = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class MediaType(models.TextChoices):
    BOOK = "book", "Book"
    MOVIE = "movie", "Movie"
    GAME = "game", "Game"


class MediaItem(models.Model):
    type = models.CharField(max_length=20, choices=MediaType.choices)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(
        upload_to="images/covers/",
        blank=True,
        null=True
    )
    total_progress = models.IntegerField(default=0)
    release_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_type_display()} '{self.title}'"


class MediaStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    IN_PROGRESS = "in_progress", "In progress"
    FINISHED = "finished", "Finished"


class UserMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="media")
    item = models.ForeignKey(MediaItem, on_delete=models.CASCADE, related_name="media")
    progress = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=MediaStatus.choices,
        default=MediaStatus.PLANNED
    )
    rating = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.item.title}"

class Note(models.Model):
    user_media = models.ForeignKey(
        UserMedia, on_delete=models.CASCADE, related_name="notes"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:30] + ("..." if len(self.text) > 30 else "")
