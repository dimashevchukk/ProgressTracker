from django.contrib import admin
from django.utils.html import format_html

from tracker.models import MediaItem, Note, Profile, User, UserMedia

admin.site.register(User)
admin.site.register(UserMedia)
admin.site.register(Note)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")
    search_fields = ["user__username", "user__email"]

    readonly_fields = ["avatar_preview"]

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
                obj.avatar.url,
            )
        return "No avatar"

    avatar_preview.short_description = "Avatar"


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ["title", "type", "release_date"]
    list_filter = ["type", "release_date"]
    search_fields = ["title"]
    readonly_fields = ["cover_preview"]

    def cover_preview(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
                obj.cover.url,
            )
        return "No image"

    cover_preview.short_description = "Cover Preview"
