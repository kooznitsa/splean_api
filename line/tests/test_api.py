import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestLineEndpoints:
    ENDPOINT = '/v1/lines/'
    PAGE_SIZE = 10
    LINES_COUNT = 282
    EXISTING_LINE_ID = 1
    NONEXISTENT_LINE_ID = -1
    LINE = 'Он пел, и строка его текла'
    SONG_NAME = 'Жертва талого льда'

    def test_list_lines_returns_success(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}?page=0&page_size={self.PAGE_SIZE}',
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('count') == self.LINES_COUNT
        assert len(response.json().get('results')) == self.PAGE_SIZE

    def test_line_info_returns_success(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}{self.EXISTING_LINE_ID}/',
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('line') == self.LINE
        assert response.json().get('song_name') == self.SONG_NAME

    def test_line_info_with_wrong_id_returns_not_found(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}{self.NONEXISTENT_LINE_ID}/',
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json().get('detail') == 'No Line matches the given query.'

    def test_list_lines_by_word_returns_success(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}by-word/?word=пел',
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get('results')) > 0

    def test_random_line_returns_success(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}random/',
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('line') is not None
        assert response.json().get('song_name') is not None

    def test_list_alcohol_lines(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}alcohol/',
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get('results'))

    def test_list_petersburg_lines(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}petersburg/',
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get('results'))

    def test_list_winter_lines(self, api_client):
        response = api_client.get(
            f'{self.ENDPOINT}winter/',
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get('results'))
