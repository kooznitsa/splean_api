from contextlib import nullcontext as does_not_raise

from django.core.exceptions import ValidationError
import pytest

from album.models import Album

pytestmark = pytest.mark.django_db


class TestAlbumModel:
    ALBUM_NAME = 'Test Album'
    ALBUM_DATE = '2025-01-01'

    test_data = (
        ('5:11', does_not_raise()),
        ('50:11', does_not_raise()),
        ('05:11', pytest.raises(ValidationError)),
        ('1:50:11', pytest.raises(ValidationError)),
        ('10:50:11', pytest.raises(ValidationError)),
        ('01:50:11', pytest.raises(ValidationError)),
    )

    @pytest.mark.parametrize('example_input,expectation', test_data)
    def test_create_album_duration(self, example_input, expectation):
        with expectation:
            album = Album(name=self.ALBUM_NAME, date=self.ALBUM_DATE, duration=example_input)

            album.full_clean()
            album.save()

            assert album
