import pandas as pd

merged_data_file_path = 'healthcare_facilities_with_population_GA.csv'

df_merged = pd.read_csv(merged_data_file_path)
print(f"Successfully loaded merged data from '{merged_data_file_path}'.")

df_merged['Total_Population'] = pd.to_numeric(df_merged['Total_Population'], errors='coerce')


original_rows_merged = len(df_merged)
df_merged.dropna(subset=['County_FIPS', 'Total_Population'], inplace=True)
print(f"Dropped {original_rows_merged - len(df_merged)} rows with missing County FIPS or Population for county-level analysis.")


print("\nPerforming county-level analysis...")

 
county_summary = df_merged.groupby(['State_FIPS', 'County_FIPS', 'County_Name']).agg(
        num_facilities=('Facility_Name', 'count'),
        Total_Population=('Total_Population', 'first') # Assuming Total_Population is consistent for a county
    ).reset_index()

county_summary['Facilities_Per_10K_People'] = (county_summary['num_facilities'] / county_summary['Total_Population']) * 10000

county_summary.loc[county_summary['Total_Population'] == 0, 'Facilities_Per_10K_People'] = 0
county_summary['Facilities_Per_10K_People'].fillna(0, inplace=True) # If population was NaN and coerced to 0

healthcare_deserts_criteria = (county_summary['num_facilities'] == 0) | \
                                  (county_summary['Facilities_Per_10K_People'] < 0.5)

potential_deserts = county_summary[healthcare_deserts_criteria].sort_values(
        by='Total_Population', ascending=False
    )

print("\n--- County Summary (Top 10 by Population) ---")
print(county_summary.sort_values(by='Total_Population', ascending=False).head(10))

print("\n--- Counties with Highest Facility Load (most facilities per 10K people, Top 10) ---")
print(county_summary.sort_values(by='Facilities_Per_10K_People', ascending=False).head(10))

print("\n--- Potential Healthcare Deserts (Counties with 0 facilities or < 0.5 facilities per 10K people) ---")
if not potential_deserts.empty:
    print(potential_deserts)
else:
    print("No potential healthcare deserts found based on the defined criteria.")


county_summary_output_filename = f'county_healthcare_summary_GA.csv'
county_summary.to_csv(county_summary_output_filename, index=False)
print(f"\nCounty summary data saved to {county_summary_output_filename}")