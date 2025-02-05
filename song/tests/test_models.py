from contextlib import nullcontext as does_not_raise

from django.core.exceptions import ValidationError
import pytest

from song.models import Song

pytestmark = pytest.mark.django_db


class TestSongModel:
    SONG_NAME = 'Test Song'
    ALBUM_ID = 1

    test_data = (
        ('5:11', does_not_raise()),
        ('50:11', does_not_raise()),
        ('05:11', pytest.raises(ValidationError)),
        ('1:50:11', pytest.raises(ValidationError)),
        ('10:50:11', pytest.raises(ValidationError)),
        ('01:50:11', pytest.raises(ValidationError)),
    )

    @pytest.mark.parametrize('example_input,expectation', test_data)
    def test_create_song_duration(self, example_input, expectation):
        with expectation:
            song = Song(name=self.SONG_NAME, album_id=self.ALBUM_ID, duration=example_input)

            song.full_clean()
            song.save()

            assert song
