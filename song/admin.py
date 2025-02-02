from django.contrib import admin

from song.models import Song

admin.site.site_header = 'Admin Panel'
admin.site.site_title = 'API admin'
admin.site.index_title = 'API administration'


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'album', 'duration')
    search_fields = ('name',)
    list_filter = ('album',)
