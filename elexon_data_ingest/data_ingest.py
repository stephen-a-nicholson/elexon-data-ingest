""" Contains a class to retrieve data from the Elexon API """

from abc import ABC, abstractmethod
from typing import Union

import pandas as pd
import requests


class DataStrategy(ABC):
    """
    Abstract base class for data processing strategies.
    """

    @abstractmethod
    def process_data(self, data: dict) -> dict:
        """
        Processes the data according to the specific strategy.

        Parameters:
            - data (dict): The raw data fetched from the API.

        Returns:
            - dict: The processed data.
        """
        return data

    @abstractmethod
    def get_strategy_info(self) -> str:
        """
        Abstract method to be implemented by subclasses.

        Returns:
            - str: Information about the strategy.
        """


class TemperatureStrategy(DataStrategy):
    """
    Data processing strategy for temperature data.
    """

    def process_data(self, data: dict) -> dict:
        """
        Processes temperature data.

        Parameters:
            - data (dict): The raw temperature data fetched from the API.

        Returns:
            - dict: The processed temperature data.
        """
        timestamp = data.get("timestamp")
        return {
            "timestamp": pd.to_datetime(timestamp),
            "temperature": data.get("temperature"),
            "temperatureReferenceAverage": data.get(
                "temperatureReferenceAverage"
            ),
        }

    def get_strategy_info(self) -> str:
        """
        Provides information about the temperature strategy.

        Returns:
            - str: Information about the temperature strategy.
        """
        return "TemperatureStrategy class"


class GenerationStrategy(DataStrategy):
    """
    Data processing strategy for generation data.

    Methods:
        - process_data(data: dict) -> dict: Processes generation data.
    """

    def process_data(self, data: dict) -> dict:
        """
        Processes generation data.

        Parameters:
            - data (dict): The raw generation data fetched from the API.

        Returns:
            - dict: The processed generation data.
        """
        timestamp = data.get("timestamp")
        types_data = data.get("data", [])
        return [
            {
                "timestamp": pd.to_datetime(timestamp),
                "type": entry["type"],
                "quantity": entry.get("quantity"),
            }
            for entry in types_data
        ]

    def get_strategy_info(self) -> str:
        """
        Provides information about the generation strategy.

        Returns:
            - str: Information about the generation strategy.
        """
        return "GenerationStrategy class"


class DemandStrategy(DataStrategy):
    """
    Data processing strategy for demand data.

    Methods:
        - process_data(data: dict) -> dict: Processes demand data.
    """

    def process_data(self, data: dict) -> dict:
        """
        Processes demand data.

        Parameters:
            - data (dict): The raw demand data fetched from the API.

        Returns:
            - dict: The processed demand data.
        """
        timestamp = data.get("timestamp")
        return {
            "timestamp": pd.to_datetime(timestamp),
            "initialDemandOutturn": data.get("initialDemandOutturn"),
        }

    def get_strategy_info(self) -> str:
        """
        Provides information about the demand strategy.

        Returns:
            - str: Information about the demand strategy.
        """
        return "DemandStrategy class"


class ElexonAPI:
    """
    A class for interacting with the Elexon API to fetch temperature, generation, and demand data.
    """

    def __init__(
        self, start_date: str, end_date: str, data_format: str = "json"
    ):
        self.base_url = "https://bmrs.elexon.co.uk/api/v1/"
        self.start_date = start_date
        self.end_date = end_date
        self.format = data_format

    def fetch_data(
        self, endpoint: str, strategy: DataStrategy
    ) -> Union[pd.DataFrame, None]:
        """
        Fetches data from the specified endpoint for the date range and format.

        Parameters:
            - endpoint (str): The specific API endpoint to fetch data from.
            - strategy (DataStrategy): The strategy for processing the data.

        Returns:
            - Union[pd.DataFrame, None]: If successful, returns the processed data as a DataFrame.
                                        If unsuccessful, returns None.
        """
        url_params = {
            "from": self.start_date,
            "to": self.end_date,
            "format": self.format,
        }

        try:
            response = requests.get(
                f"{self.base_url}{endpoint}", params=url_params, timeout=5
            )
            response.raise_for_status()
            data = response.json()
            processed_data = strategy.process_data(data)

            if isinstance(processed_data, list):
                return pd.DataFrame(processed_data)

            return pd.DataFrame([processed_data])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def get_temperature_data(self) -> Union[pd.DataFrame, None]:
        """Fetches temperature data."""
        return self.fetch_data("temperature", TemperatureStrategy())

    def get_generation_data(self) -> Union[pd.DataFrame, None]:
        """Fetches generation data."""
        return self.fetch_data(
            "generation/actual/per-type", GenerationStrategy()
        )

    def get_demand_data(self) -> Union[pd.DataFrame, None]:
        """Fetches demand data."""
        return self.fetch_data("demand", DemandStrategy())
