import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
CENSUS_API_KEY = os.getenv('CENSUS_API_KEY')

if not CENSUS_API_KEY:
    raise ValueError("Census API key not found. Please set it in a .env file.")
STATE_FIPS = '13' # Georgia's FIPS code. If I need all states I can use *.
YEAR = '2022'

base_url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
params = {
    'get': 'NAME,B01001_001E',
    'for': f'county:*',
    'in': f'state:{STATE_FIPS}',
    'key': CENSUS_API_KEY
}

output_filename = f'census_population_data_state_{STATE_FIPS}_{YEAR}.csv'
sqlite_db_name = 'healthcare_data.db'
table_name = 'census_population_county'

print(f"Fetching county-level population data for state FIPS: {STATE_FIPS} for year {YEAR}...")

try:
    response = requests.get(base_url, params=params)
    response.raise_for_status() 
    data = response.json()

    headers = data[0]
    rows = data[1:]

    df = pd.DataFrame(rows, columns=headers)

    df = df.rename(columns={
        'B01001_001E': 'Total_Population',
        'NAME': 'County_Name',
        'state': 'State_FIPS',
        'county': 'County_FIPS'
    })

    df['Total_Population'] = pd.to_numeric(df['Total_Population'], errors='coerce')

    print(f"Successfully fetched {len(df)} county records.")


    df.to_csv(output_filename, index=False)
    print(f"Data saved to {output_filename}")

    from sqlalchemy import create_engine
    engine = create_engine(f'sqlite:///{sqlite_db_name}')
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Data saved to SQLite table '{table_name}' in {sqlite_db_name}")

    print("\nFirst 5 rows of the DataFrame:")
    print(df.head())

except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
    print(f"Response content: {response.text}")
except requests.exceptions.RequestException as err:
    print(f"An error occurred during the request: {err}")
except ValueError as err:
    print(f"Error parsing JSON or processing data: {err}")
    print(f"Raw response text: {response.text}")
except Exception as err:
    print(f"An unexpected error occurred: {err}")