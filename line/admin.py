from django.contrib import admin

from line.models import Line


@admin.register(Line)
class SongAdmin(admin.ModelAdmin):
    list_display = ('line', 'song',)
    search_fields = ('line',)
    list_filter = ('song',)
