# elexon-data-ingest

This Python application extracts data from the Elexon API using the requests library to interact with specific endpoints, each catering to different datasets such as temperature, generation, and demand. Employing the strategy pattern allows for the encapsulation of algorithms related to each endpoint, enabling seamless switching between them. This modular design facilitates extensibility, making it easier to incorporate new endpoints in the future without disrupting the existing codebase.

Settlement periods represent discrete time intervals during which energy consumption and generation data are recorded. In the context of Elexon's data, settlement periods are typically 30 minutes long, and their aggregation provides insights into the energy landscape. Understanding settlement periods is vital for analysing and modelling energy-related phenomena, as these periods influence pricing, demand forecasting, and overall grid management.

# Project Requirements and Usage Guide

## Requirements

- **Python:** The project requires either Python 3.10 or Python 3.11. Ensure that you have Python installed on your system.

- **Poetry:** Make sure Poetry is installed. If not, you can install it using the following command:
  ```bash
  python -m pip install --upgrade poetry

  cd <project_directory>

  poetry install

  poetry shell

  usage: ingest_data.py [-h] --from FROM_DATE --to TO_DATE --key API_KEY
  ```