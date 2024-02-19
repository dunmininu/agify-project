from datetime import datetime, timedelta

from django.core.cache import cache
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from .models import AgeGuess

import pytest
from unittest.mock import patch

@pytest.mark.django_db
class TestGuessAgeView:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('guess-age')
        cache.clear()

    def perform_valid_request(self, mock_get):
        mock_response = {"name": "michael", "age": 50, "count": 12345}
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200
        return self.client.post(self.url, {"name": "michael"}, format='json')

    @patch('agify_app.views.requests.get')
    def test_guess_age_valid_request(self, mock_get):
        response = self.perform_valid_request(mock_get)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == "michael"
        assert response.data['age'] == 50
        current_year = datetime.now().year
        expected_dob = current_year - 50
        assert response.data['date_of_birth'] == expected_dob

    @patch('agify_app.views.requests.get')
    def test_guess_age_caching(self, mock_get):
        self.perform_valid_request(mock_get)
        mock_get.reset_mock()
        response = self.client.post(self.url, {"name": "michael"}, format='json')
        mock_get.assert_not_called()
        assert response.status_code == status.HTTP_200_OK

    def test_guess_age_invalid_request(self):
        response = self.client.post(self.url, {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    @patch('agify_app.views.requests.get')
    def test_age_guess_model_update(self, mock_get):
        mock_response = {"name": "michael", "age": 50, "count": 12345}
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        self.perform_valid_request(mock_get)

        age_guess = AgeGuess.objects.get(name="michael")
        assert age_guess.age == 50
        assert age_guess.date_of_birth == datetime.now().date() - timedelta(days=365*50)
