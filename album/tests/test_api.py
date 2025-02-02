import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestAlbumEndpoints:
    ENDPOINT = '/v1/albums/'
    ALBUMS_COUNT = 17
    EXISTING_ALBUM_ID = 1
    NONEXISTENT_ALBUM_ID = 100
    ALBUM_NAME = 'Пыльная быль'
    ALBUM_DATE = '1994-05-01'

    def test_list_albums_returns_success(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}?page=0&page_size=100',
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get('results')) == self.ALBUMS_COUNT

    def test_list_album_songs_returns_success(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}{self.EXISTING_ALBUM_ID}/songs/',
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get('results')) > 0

    def test_list_album_songs_with_wrong_id_returns_empty(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}{self.NONEXISTENT_ALBUM_ID}/songs/',
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get('results')) == 0

    def test_album_info_returns_success(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}{self.EXISTING_ALBUM_ID}/',
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('name') == self.ALBUM_NAME
        assert response.json().get('date') == self.ALBUM_DATE

    def test_album_info_with_wrong_id_returns_not_found(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}{self.NONEXISTENT_ALBUM_ID}/',
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get('detail') == 'No Album matches the given query.'
