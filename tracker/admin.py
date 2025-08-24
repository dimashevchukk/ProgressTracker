from django.contrib import admin

from tracker.models import (
    User,
    Profile,
    MediaItem,
    UserMedia,
    Note
)

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(MediaItem)
admin.site.register(UserMedia)
admin.site.register(Note)
