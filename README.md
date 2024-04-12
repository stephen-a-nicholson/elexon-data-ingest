# Elexon Data Ingestion

This project ingests data from the Elexon API, processes it, and stores it in a SQLite database. The data includes temperature, generation, and demand data. The project utilises the Strategy pattern to handle different data processing strategies for each API endpoint.

## Prerequisites

- Python 3.7 or higher
- Poetry (Python dependency management tool)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/stephen-a-nicholson/elexon-data-ingest.git
   cd elexon-data-ingest
   ```

2. Install the dependencies using Poetry:

   ```bash
   poetry install
   ```

## Usage

1. Activate the virtual environment created by Poetry:

   ```bash
   poetry shell
   ```

2. Run the data ingestion script with the required command-line arguments:

   ```bash
   python ingest_data.py --from START_DATE --to END_DATE --key API_KEY
   ```

   Replace `START_DATE` and `END_DATE` with the desired date range in the format `YYYY-MM-DD`, and `API_KEY` with your Elexon API key.

   Example:
   ```bash
   python ingest_data.py --from 2023-01-01 --to 2023-01-31 --key your_api_key
   ```

3. The script will fetch the data from the Elexon API, process it using the appropriate strategy for each endpoint, and store it in an in-memory SQLite database. The consolidated data will be logged, and a sample of the data will be printed from the database.

## Project Structure

- `elexon_api.py`: Contains the `ElexonAPI` class for interacting with the Elexon API and fetching data. It also includes data processing strategies for temperature, generation, and demand data, implemented using the Strategy pattern.
- `ingest_data.py`: The main script that uses the `ElexonAPI` class to fetch data, process it using the appropriate strategy, and store it in a SQLite database.

## Logging

The project uses logging to capture relevant information during the data ingestion process. The log messages are written to a file named `elexon.log`.

## Licence

This project is licensed under the [MIT Licence](https://github.com/stephen-a-nicholson/elexon-data-ingest/blob/main/LICENCE).