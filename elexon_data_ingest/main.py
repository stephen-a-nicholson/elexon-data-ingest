""" Main """

import pandas as pd

from elexon_data_ingest.data_ingest import ElexonAPI

START_DATE = "2022-09-20"
END_DATE = "2022-09-21"


def main() -> None:
    """Entry point"""
    elexon_api = ElexonAPI(START_DATE, END_DATE)
    temperature_data = elexon_api.get_temperature_data()
    generation_data = elexon_api.get_generation_data()
    demand_data = elexon_api.get_demand_data()

    # Merging dataframes on timestamp
    merged_data = pd.merge(
        temperature_data, generation_data, on="timestamp", how="outer"
    )
    merged_data = pd.merge(
        merged_data, demand_data, on="timestamp", how="outer"
    )

    print("Consolidated Data:")
    print(merged_data)


if __name__ == "__main__":
    main()
