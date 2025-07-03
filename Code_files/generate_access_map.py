import pandas as pd
import geopandas
import folium
from folium.plugins import MarkerCluster


county_summary_file_path = 'county_healthcare_summary_GA.csv'
merged_facilities_file_path = 'healthcare_facilities_with_population_GA.csv'


georgia_shapefile_path = 'tl_2022_us_county/tl_2022_us_county.shp'

df_county_summary = pd.read_csv(county_summary_file_path)
df_facilities = pd.read_csv(merged_facilities_file_path) # Load original merged facilities for points
print(f"Successfully loaded county summary from '{county_summary_file_path}'.")
print(f"Successfully loaded facilities data from '{merged_facilities_file_path}'.")


df_county_summary['State_FIPS'] = df_county_summary['State_FIPS'].astype(str)
df_county_summary['County_FIPS'] = df_county_summary['County_FIPS'].astype(str)


gdf_counties = geopandas.read_file(georgia_shapefile_path)
print(f"Successfully loaded Georgia county shapefile from '{georgia_shapefile_path}'.")

gdf_counties['GEOID'] = gdf_counties['GEOID'].astype(str)
df_county_summary['Full_FIPS'] = df_county_summary['State_FIPS'] + df_county_summary['County_FIPS']

gdf_merged_counties = gdf_counties.merge(
        df_county_summary,
        left_on='GEOID',
        right_on='Full_FIPS',
        how='left'
    )
print("Merged geospatial data with county summary.")

gdf_merged_counties['num_facilities'].fillna(0, inplace=True)
gdf_merged_counties['Total_Population'].fillna(0, inplace=True)
gdf_merged_counties['Facilities_Per_10K_People'].fillna(0, inplace=True)

print("\nCreating interactive map...")

map_center = [32.9866, -83.6487] # Approximate center of Georgia

m = folium.Map(location=map_center, zoom_start=7, tiles='CartoDB positron')

folium.Choropleth(
        geo_data=gdf_merged_counties,
        name='Facilities per 10K People',
        data=gdf_merged_counties,
        columns=['GEOID', 'Facilities_Per_10K_People'],
        key_on='feature.properties.GEOID',
        fill_color='YlGnBu', # Yellow-Green-Blue color scheme
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Health Centers per 10,000 People',
        highlight=True,
        tooltip=folium.GeoJsonTooltip(fields=['NAME', 'Total_Population', 'num_facilities', 'Facilities_Per_10K_People'],
                                     aliases=['County:', 'Population:', 'Facilities:', 'Facilities/10K:'],
                                     localize=True)
    ).add_to(m)

df_facilities_for_map = df_facilities.dropna(subset=['Latitude', 'Longitude'])

marker_cluster = MarkerCluster().add_to(m)

for idx, row in df_facilities_for_map.iterrows():
    if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
            popup_text = f"<b>{row['Facility_Name']}</b><br>" \
                         f"Address: {row['Address']}, {row['City']}, {row['State_Abbrev']} {row['ZIP_Code']}<br>" \
                         f"County: {row['County_Name']}"
            folium.Marker(location=[row['Latitude'], row['Longitude']], popup=popup_text, tooltip=row['Facility_Name']).add_to(marker_cluster)

folium.LayerControl().add_to(m)

map_output_filename = 'georgia_healthcare_access_map.html'
m.save(map_output_filename)
print(f"\nInteractive map saved to {map_output_filename}. You can open this file in your web browser.")
