import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestSongEndpoints:
    ENDPOINT = '/v1/songs/'
    SONGS_COUNT = 217
    SONG_LINES_COUNT = 10
    PAGE_SIZE = 10
    EXISTING_SONG_ID = 1
    NONEXISTENT_SONG_ID = 1000
    SONG_NAME = 'Жертва талого льда'
    SONG_DURATION = '6:01'
    SONG_ALBUM_NAME = 'Пыльная быль'

    def test_list_albums_returns_success(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}?page=0&page_size={self.PAGE_SIZE}',
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('count') == self.SONGS_COUNT
        assert len(response.json().get('results')) == self.PAGE_SIZE

    def test_list_song_lines_returns_success(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}{self.EXISTING_SONG_ID}/lines/',
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get('results')) > 0

    def test_list_song_lines_with_wrong_id_returns_empty(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}{self.NONEXISTENT_SONG_ID}/lines/',
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get('results')) == 0

    def test_song_info_returns_success(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}{self.EXISTING_SONG_ID}/',
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('name') == self.SONG_NAME
        assert response.json().get('duration') == self.SONG_DURATION
        assert response.json().get('album_name') == self.SONG_ALBUM_NAME

    def test_song_info_with_wrong_id_returns_not_found(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}{self.NONEXISTENT_SONG_ID}/',
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get('detail') == 'No Song matches the given query.'

    def test_list_songs_by_year_returns_success(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}by-year/?year=1999',
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get('results')) == self.SONG_LINES_COUNT

    def test_list_songs_by_wrong_year_returns_empty(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}by-year/?year=1812',
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get('results')) == 0

    def test_get_songs_stats_returns_success(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}stats/',
        )

        assert response.status_code == status.HTTP_200_OK
