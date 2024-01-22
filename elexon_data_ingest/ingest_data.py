""" Ingests data from the Elexon API """

import argparse

import pandas as pd
from sqlalchemy import create_engine, text

from elexon_data_ingest.elexon_api import ElexonAPI, logger


def ingest_elexon_data() -> None:
    """Ingests quantity per type, temperate and initial demand outturn from Elexon API"""
    parser = argparse.ArgumentParser(
        description="Process data with command line arguments"
    )

    parser.add_argument(
        "--from",
        dest="from_date",
        type=str,
        required=True,
        help="Start date (format: YYYY-MM-DD)",
    )

    parser.add_argument(
        "--to",
        dest="to_date",
        type=str,
        required=True,
        help="End date (format: YYYY-MM-DD)",
    )

    parser.add_argument(
        "--key",
        dest="api_key",
        type=str,
        required=True,
        help="API key for authentication",
    )

    args = parser.parse_args()

    elexon_api: ElexonAPI = ElexonAPI(
        auth=args.api_key, start_date=args.from_date, end_date=args.to_date
    )

    temperature_data: pd.DataFrame = elexon_api.get_temperature_data()
    generation_data: pd.DataFrame = elexon_api.get_generation_data()
    demand_data: pd.DataFrame = elexon_api.get_demand_data()

    merged_data: pd.DataFrame = (
        pd.merge(
            generation_data,
            temperature_data,
            left_on=pd.to_datetime(generation_data["timestamp"]).dt.date,
            right_on="timestamp",
            how="left",
        )
        .drop(["timestamp", "timestamp_y"], axis=1)
        .rename(columns={"timestamp_x": "timestamp"})
    )

    merged_data: pd.DataFrame = pd.merge(
        merged_data, demand_data, on="timestamp", how="outer"
    ).dropna()
    merged_data.set_index("timestamp", inplace=True)

    logger.info("Consolidated data:\n%s\n", merged_data)

    engine = create_engine("sqlite://", echo=False)

    merged_data.to_sql("elexon", con=engine)

    with engine.connect() as conn:
        logger.info(
            conn.execute(text("""SELECT * FROM elexon LIMIT 15""")).fetchall()
        )


if __name__ == "__main__":
    ingest_elexon_data()
