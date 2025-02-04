from django.contrib import admin

from album.models import Album


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'duration',)
    search_fields = ('name', 'date',)
    list_filter = ('date',)
