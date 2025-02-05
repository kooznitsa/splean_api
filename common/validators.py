import re
from typing import NoReturn

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_duration(value: str) -> NoReturn:
    if not re.match(r'^[1-9]\d?:\d{2}$', value):
        raise ValidationError(
            _('%(value)s is not a valid duration'),
            params={'value': value},
        )
