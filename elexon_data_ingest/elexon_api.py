""" Contains a class to retrieve data from the Elexon API """

from abc import ABC, abstractmethod
from typing import Any, Union

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth


class DataStrategy(ABC):
    """
    Abstract base class for data processing strategies.
    """

    @abstractmethod
    def process_data(self, data: dict) -> pd.DataFrame:
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

    def process_data(self, data: dict) -> pd.DataFrame:
        """
        Processes temperature data.

        Parameters:
            - data (dict): The raw temperature data fetched from the API.

        Returns:
            - dict: The processed temperature data.
        """
        extracted_data: list[dict[str, Any]] = [
            {
                "temperature": entry["temperature"],
                "temperatureReferenceAverage": entry[
                    "temperatureReferenceAverage"
                ],
                "timestamp": pd.to_datetime(entry["measurementDate"]).date(),
            }
            for entry in data["data"]
        ]

        return pd.DataFrame(extracted_data)

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

    def process_data(self, data: dict) -> pd.DataFrame:
        """
        Processes generation data.

        Parameters:
            - data (dict): The raw generation data fetched from the API.

        Returns:
            - dict: The processed generation data.
        """
        extracted_data: list[dict[str, Any]] = [
            {
                "timestamp": pd.to_datetime(entry["startTime"]),
                "psrType": subentry["psrType"],
                "quantity": subentry["quantity"],
            }
            for entry in data["data"]
            for subentry in entry["data"]
        ]

        return pd.DataFrame(extracted_data)

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

    def process_data(self, data: dict) -> pd.DataFrame:
        """
        Processes demand data.

        Parameters:
            - data (dict): The raw demand data fetched from the API.

        Returns:
            - dict: The processed demand data.
        """
        extracted_data: list[dict[str, Any]] = [
            {
                "timestamp": pd.to_datetime(entry["startTime"]),
                "initialDemandOutturn": entry.get("initialDemandOutturn"),
            }
            for entry in data["data"]
        ]

        return pd.DataFrame(extracted_data)

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
        self,
        auth: str,
        start_date: str,
        end_date: str,
        data_format: str = "json",
    ):
        self.base_url = "https://data.elexon.co.uk/bmrs/api/v1/"
        self.auth = HTTPBasicAuth("apikey", auth)
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
        url_params: dict[str, str] = {
            "from": self.start_date,
            "to": self.end_date,
            "format": self.format,
        }

        if endpoint == "demand/outturn":
            url_params["settlementDateFrom"] = url_params.pop("from")
            url_params["settlementDateTo"] = url_params.pop("to")

        try:
            response: requests.Response = requests.get(
                f"{self.base_url}{endpoint}",
                params=url_params,
                timeout=5,
                auth=self.auth,
            )
            response.raise_for_status()
            data: Any = response.json()
            processed_data: pd.DataFrame = strategy.process_data(data)

            return processed_data
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
        return self.fetch_data("demand/outturn", DemandStrategy())
