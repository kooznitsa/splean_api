from django.db import models


class Song(models.Model):
    name = models.CharField(max_length=100)
    album = models.ForeignKey('album.Album', on_delete=models.CASCADE)
    duration = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'songs'
        verbose_name_plural = 'Songs'
        unique_together = ('name', 'album',)
