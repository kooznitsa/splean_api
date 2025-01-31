from django.db import models


class Line(models.Model):
    line = models.TextField()
    song = models.ForeignKey('song.Song', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.line[:20]}...'

    class Meta:
        db_table = 'lines'
        verbose_name_plural = 'Lines'
