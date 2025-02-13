from django.db import models

from common.validators import validate_duration


class Album(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=10, null=True, blank=True, validators=[validate_duration])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'albums'
        verbose_name_plural = 'Albums'
