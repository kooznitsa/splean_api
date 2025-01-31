from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'albums'
        verbose_name_plural = 'Albums'
