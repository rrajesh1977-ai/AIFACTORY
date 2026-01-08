import unittest
from unittest.mock import patch, Mock
import requests
from find_businesses import find_local_businesses

class TestFindLocalBusinesses(unittest.TestCase):

    @patch('requests.get')
    def test_find_local_businesses_success(self, mock_get):
        # Mocking a successful response
        mock_response = Mock()
        expected_json = {
            "status": "OK",
            "results": [
                {
                    "name": "Test Cafe",
                    "formatted_address": "123 Test St, Test City",
                    "rating": 4.5,
                    "user_ratings_total": 100
                },
                {
                    "name": "Another Cafe",
                    "formatted_address": "456 Other St, Test City",
                    "rating": 4.0,
                    "user_ratings_total": 50
                }
            ]
        }
        mock_response.json.return_value = expected_json
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        businesses = find_local_businesses("dummy_api_key", "Test City", "cafe")

        self.assertIsNotNone(businesses)
        self.assertEqual(len(businesses), 2)
        self.assertEqual(businesses[0]['name'], "Test Cafe")
        self.assertEqual(businesses[0]['address'], "123 Test St, Test City")
        self.assertEqual(businesses[1]['name'], "Another Cafe")

    @patch('requests.get')
    def test_find_local_businesses_zero_results(self, mock_get):
        # Mocking a response with zero results
        mock_response = Mock()
        expected_json = {
            "status": "ZERO_RESULTS",
            "results": []
        }
        mock_response.json.return_value = expected_json
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        businesses = find_local_businesses("dummy_api_key", "Empty City", "rare_business")

        self.assertIsNotNone(businesses)
        self.assertEqual(len(businesses), 0)

    @patch('requests.get')
    def test_find_local_businesses_api_error(self, mock_get):
        # Mocking an API error response (e.g., invalid key)
        mock_response = Mock()
        expected_json = {
            "status": "REQUEST_DENIED",
            "error_message": "The provided API key is invalid."
        }
        mock_response.json.return_value = expected_json
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        businesses = find_local_businesses("invalid_key", "Test City", "cafe")

        self.assertIsNone(businesses)

    @patch('requests.get')
    def test_find_local_businesses_network_error(self, mock_get):
        # Mocking a network exception
        mock_get.side_effect = requests.exceptions.RequestException("Connection refused")

        businesses = find_local_businesses("dummy_api_key", "Test City", "cafe")

        self.assertIsNone(businesses)

if __name__ == '__main__':
    unittest.main()
