import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from elexon_data_ingest.elexon_api import (
    DemandStrategy,
    ElexonAPI,
    GenerationStrategy,
    TemperatureStrategy,
)


class TestElexonAPI(unittest.TestCase):
    """
    Test case for the ElexonAPI class.
    """

    def setUp(self):
        """
        Set up the necessary attributes for the tests.
        """
        self.api_key = "your_api_key"
        self.start_date = "2023-01-01"
        self.end_date = "2023-01-31"
        self.elexon_api = ElexonAPI(self.api_key, self.start_date, self.end_date)

    @patch("elexon_data_ingest.elexon_api.requests.get")
    def test_fetch_data(self, mock_get):
        """
        Test the fetch_data method of the ElexonAPI class.
        """
        # Mock the response from the API
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response

        # Test fetching temperature data
        temperature_data = self.elexon_api.fetch_data(
            "temperature", TemperatureStrategy()
        )
        self.assertIsInstance(temperature_data, pd.DataFrame)

        # Test fetching generation data
        generation_data = self.elexon_api.fetch_data(
            "generation/actual/per-type", GenerationStrategy()
        )
        self.assertIsInstance(generation_data, pd.DataFrame)

        # Test fetching demand data
        demand_data = self.elexon_api.fetch_data("demand/outturn", DemandStrategy())
        self.assertIsInstance(demand_data, pd.DataFrame)

    @patch.object(ElexonAPI, "fetch_data")
    def test_get_temperature_data(self, mock_fetch_data):
        """
        Test the get_temperature_data method of the ElexonAPI class.
        """
        mock_fetch_data.return_value = pd.DataFrame()
        temperature_data = self.elexon_api.get_temperature_data()
        self.assertIsInstance(temperature_data, pd.DataFrame)
        mock_fetch_data.assert_called_once()
        args, _ = mock_fetch_data.call_args
        self.assertEqual(args[0], "temperature")
        self.assertIsInstance(args[1], TemperatureStrategy)

    @patch.object(ElexonAPI, "fetch_data")
    def test_get_generation_data(self, mock_fetch_data):
        """
        Test the get_generation_data method of the ElexonAPI class.
        """
        mock_fetch_data.return_value = pd.DataFrame()
        generation_data = self.elexon_api.get_generation_data()
        self.assertIsInstance(generation_data, pd.DataFrame)
        mock_fetch_data.assert_called_once()
        args, _ = mock_fetch_data.call_args
        self.assertEqual(args[0], "generation/actual/per-type")
        self.assertIsInstance(args[1], GenerationStrategy)

    @patch.object(ElexonAPI, "fetch_data")
    def test_get_demand_data(self, mock_fetch_data):
        """
        Test the get_demand_data method of the ElexonAPI class.
        """
        mock_fetch_data.return_value = pd.DataFrame()
        demand_data = self.elexon_api.get_demand_data()
        self.assertIsInstance(demand_data, pd.DataFrame)
        mock_fetch_data.assert_called_once()
        args, _ = mock_fetch_data.call_args
        self.assertEqual(args[0], "demand/outturn")
        self.assertIsInstance(args[1], DemandStrategy)


class TestDataStrategies(unittest.TestCase):
    """
    Test case for the data processing strategies.
    """

    def test_temperature_strategy(self):
        """
        Test the process_data method of the TemperatureStrategy class.
        """
        data = {
            "data": [
                {
                    "temperature": 20,
                    "temperatureReferenceAverage": 18,
                    "measurementDate": "2023-01-01",
                }
            ]
        }
        temperature_data = TemperatureStrategy().process_data(data)
        self.assertIsInstance(temperature_data, pd.DataFrame)
        self.assertEqual(len(temperature_data), 1)

    def test_generation_strategy(self):
        """
        Test the process_data method of the GenerationStrategy class.
        """
        data = {
            "data": [
                {
                    "startTime": "2023-01-01T00:00:00",
                    "data": [{"psrType": "CCGT", "quantity": 100}],
                }
            ]
        }
        generation_data = GenerationStrategy().process_data(data)
        self.assertIsInstance(generation_data, pd.DataFrame)
        self.assertEqual(len(generation_data), 1)

    def test_demand_strategy(self):
        """
        Test the process_data method of the DemandStrategy class.
        """
        data = {
            "data": [
                {
                    "startTime": "2023-01-01T00:00:00",
                    "initialDemandOutturn": 5000,
                }
            ]
        }
        demand_data = DemandStrategy().process_data(data)
        self.assertIsInstance(demand_data, pd.DataFrame)
        self.assertEqual(len(demand_data), 1)


if __name__ == "__main__":
    unittest.main()
