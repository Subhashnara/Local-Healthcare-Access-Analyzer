import pandas as pd


county_summary_file_path = 'county_healthcare_summary_GA.csv'
rucc_file_path = 'Ruralurbancontinuumcodes2023.csv'



df_county_summary = pd.read_csv(county_summary_file_path)
df_rucc_raw = pd.read_csv(rucc_file_path, encoding='latin1')
print(f"Successfully loaded county summary from '{county_summary_file_path}'.")
print(f"Successfully loaded RUCC raw data from '{rucc_file_path}'.")

    
print("\nProcessing RUCC data to wide format...")

df_rucc_codes = df_rucc_raw[df_rucc_raw['Attribute'] == 'RUCC_2023'][['FIPS', 'Value']].rename(columns={'Value': 'RUCC_Code_Str'})
df_rucc_descriptions = df_rucc_raw[df_rucc_raw['Attribute'] == 'Description'][['FIPS', 'Value']].rename(columns={'Value': 'RUCC_Description'})

df_rucc_processed = pd.merge(df_rucc_codes, df_rucc_descriptions, on='FIPS', how='inner')

df_rucc_processed['FIPS'] = df_rucc_processed['FIPS'].astype(str)
df_rucc_processed['RUCC_Code'] = pd.to_numeric(df_rucc_processed['RUCC_Code_Str'], errors='coerce')
df_rucc_processed.drop(columns=['RUCC_Code_Str'], inplace=True) # Drop temporary string column

print("RUCC data processed. First 5 rows:")
print(df_rucc_processed.head())
print("\nInformation about processed RUCC DataFrame:")
print(df_rucc_processed.info())

df_county_summary['Full_FIPS'] = df_county_summary['State_FIPS'].astype(str) + df_county_summary['County_FIPS'].astype(str)
df_county_summary['Full_FIPS'] = df_county_summary['Full_FIPS'].astype(str)



print("\nMerging RUCC data with county healthcare summary...")
merged_county_summary_rucc = pd.merge(df_county_summary, df_rucc_processed, left_on='Full_FIPS', right_on='FIPS', how='left'    )

merged_county_summary_rucc.drop(columns=['FIPS'], inplace=True)

print(f"Merge complete. Total rows in merged county summary: {len(merged_county_summary_rucc)}")

print("\nAnalyzing Urban vs. Rural Gaps...")


merged_county_summary_rucc['Urban_Rural_Category'] = merged_county_summary_rucc['RUCC_Code'].apply(
        lambda x: 'Metropolitan' if pd.notna(x) and x <= 3 else ('Nonmetropolitan' if pd.notna(x) and x > 3 else 'Unknown')
    )


urban_rural_analysis = merged_county_summary_rucc.groupby('Urban_Rural_Category').agg(
        Average_Facilities_Per_10K_People=('Facilities_Per_10K_People', 'mean'),
        Total_Counties=('County_Name', 'count'),
        Total_Facilities=('num_facilities', 'sum'),
        Total_Population=('Total_Population', 'sum')
    ).reset_index()

print("\n--- Urban vs. Rural Healthcare Access Analysis ---")
print(urban_rural_analysis)


print("\n--- Top 10 Most Underserved Nonmetropolitan Counties by Facilities per 10K People ---")
underserved_nonmetro = merged_county_summary_rucc[
        (merged_county_summary_rucc['Urban_Rural_Category'] == 'Nonmetropolitan') &
        (merged_county_summary_rucc['num_facilities'] == 0) &
        (merged_county_summary_rucc['Total_Population'] > 0) &
        (merged_county_summary_rucc['State_FIPS'] == '13') # Filter for Georgia
    ].sort_values(by='Total_Population', ascending=False)

if not underserved_nonmetro.empty:
    print(underserved_nonmetro[['County_Name', 'Total_Population', 'num_facilities', 'Facilities_Per_10K_People', 'RUCC_Description']].head(10))
else:
    print("No nonmetropolitan counties in Georgia found with 0 facilities based on this dataset.")



updated_county_summary_output_filename = 'county_healthcare_summary_GA_with_rucc.csv'
merged_county_summary_rucc.to_csv(updated_county_summary_output_filename, index=False)
print(f"\nUpdated county summary data (with RUCC) saved to {updated_county_summary_output_filename}")


