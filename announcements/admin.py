from django.contrib import admin
from .models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['announcement_id', 'title', 'author', 'publish_date']
    search_fields = ['announcement_id', 'title']

admin.site.register(Announcement, AnnouncementAdmin)
