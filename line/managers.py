from django.core.cache import cache
from django.db import models


class LineManager(models.Manager):
    def values_from_cache(self, key: str) -> dict:
        cache_key = 'LineValuesCache'
        values = cache.get(cache_key)

        if values:
            d = {
                'in_cache': True,
                'values': values,
            }
        else:
            values = super().get_queryset().values_list(key, flat=True)
            cache.set(cache_key, values, 300) # 5 min cache
            d = {
                'in_cache': False,
                'values': values,
            }
        return d
