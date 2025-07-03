import pandas as pd

hrsa_locations_file_path = 'Health_Center_Service_Delivery_and_LookAlike_Sites.csv'
census_population_file_path = 'census_population_data_state_13_2022.csv' 

STATE_FIPS_TO_FILTER = '13' 
STATE_ABBREV_TO_FILTER = 'GA' 


df_hrsa_locations = pd.read_csv(hrsa_locations_file_path)
df_census_population = pd.read_csv(census_population_file_path)
print("Successfully loaded HRSA locations and Census population data.")


print("\nProcessing HRSA Locations data...")


df_hrsa_locations['State FIPS Code'] = df_hrsa_locations['State FIPS Code'].astype(str)
df_hrsa_filtered = df_hrsa_locations[
        df_hrsa_locations['State FIPS Code'] == STATE_FIPS_TO_FILTER
    ].copy()

print(f"Filtered HRSA data for State FIPS: {STATE_FIPS_TO_FILTER}. Original rows: {len(df_hrsa_locations)}, Filtered rows: {len(df_hrsa_filtered)}")


selected_hrsa_cols = {
        'Site Name': 'Facility_Name',
        'Site Address': 'Address',
        'Site City': 'City',
        'Site State Abbreviation': 'State_Abbrev',
        'Site Postal Code': 'ZIP_Code',
        'Geocoding Artifact Address Primary X Coordinate': 'Longitude',
        'Geocoding Artifact Address Primary Y Coordinate': 'Latitude',  
        'State FIPS Code': 'State_FIPS', 
        'State and County Federal Information Processing Standard Code': 'County_FIPS_Full'
    }
df_hrsa_processed = df_hrsa_filtered[list(selected_hrsa_cols.keys())].rename(columns=selected_hrsa_cols)


df_hrsa_processed['County_FIPS'] = df_hrsa_processed['County_FIPS_Full'].str[-3:]

df_hrsa_processed['Longitude'] = pd.to_numeric(df_hrsa_processed['Longitude'], errors='coerce')
df_hrsa_processed['Latitude'] = pd.to_numeric(df_hrsa_processed['Latitude'], errors='coerce')

original_rows = len(df_hrsa_processed)
df_hrsa_processed.dropna(subset=['Latitude', 'Longitude'], inplace=True)
print(f"Dropped {original_rows - len(df_hrsa_processed)} rows with missing Latitude/Longitude from HRSA data.")

df_hrsa_processed.drop(columns=['County_FIPS_Full'], inplace=True)

print("\nProcessing Census Population data...")
df_census_population['County_FIPS'] = df_census_population['County_FIPS'].astype(str)
df_census_population['State_FIPS'] = df_census_population['State_FIPS'].astype(str)

print("\nMerging HRSA and Census data...")

merged_df = pd.merge(
        df_hrsa_processed,
        df_census_population[['State_FIPS', 'County_FIPS', 'County_Name', 'Total_Population']],
        on=['State_FIPS', 'County_FIPS'],
        how='left'
    )

print(f"Merge complete. Total rows in merged DataFrame: {len(merged_df)}")

print("\nFirst 5 rows of the Merged DataFrame:")
print(merged_df.head())
print("\nInformation about the Merged DataFrame:")
print(merged_df.info())

output_merged_filename = f'healthcare_facilities_with_population_{STATE_ABBREV_TO_FILTER}.csv'
merged_df.to_csv(output_merged_filename, index=False)
print(f"\nMerged data saved to {output_merged_filename}")