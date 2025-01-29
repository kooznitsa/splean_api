from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'albums'
        verbose_name_plural = 'Albums'


class Song(models.Model):
    name = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    duration = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'songs'
        verbose_name_plural = 'Songs'
        unique_together = ('name', 'album',)


class Line(models.Model):
    line = models.TextField()
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.line[:20]}...'

    class Meta:
        db_table = 'lines'
        verbose_name_plural = 'Lines'
