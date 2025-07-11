# Geospatial Analysis of Healthcare Accessibility in Georgia

I'm facing some issues with the streamlit dashboards, as of now I'm attaching the screenshots:

# Geospatial Analysis of Georgia:

![Screenshot 2025-07-07 142154](https://github.com/user-attachments/assets/437ea086-ac9b-4e69-a38d-44fd73cd70eb)

# The dashboards which define the analytics for Georgia State:

![Screenshot 2025-07-07 142348](https://github.com/user-attachments/assets/c7ea7158-42fb-4a0e-aa99-0a03e9ab3514)

![image](https://github.com/user-attachments/assets/6832014c-a199-4381-9550-a8fa29ba2c92)

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Problem Statement](#problem-statement)  
- [Key Features](#key-features)  
- [Technologies Used](#technologies-used)  
- [Project Pipeline](#project-pipeline)  
- [Local Setup and Execution](#local-setup-and-execution)  
- [Key Insights](#key-insights)  

---

## Project Overview

This project provides a comprehensive analysis of healthcare accessibility across all 159 counties in Georgia. By integrating data from the U.S. Census Bureau, the Health Resources and Services Administration (HRSA), and the USDA, this analysis identifies potential *"healthcare deserts"*—areas with a low ratio of health centers to population.

The final output is an interactive web dashboard built with Streamlit, designed to empower public health officials, policymakers, and researchers to explore and understand regional disparities in healthcare access.

---

## Problem Statement

Access to healthcare is not uniform. How can we identify which communities in Georgia are most underserved in terms of healthcare facilities? This project addresses this by answering three key questions:

1. What is the distribution of healthcare facilities relative to population size in each county?  
2. How does healthcare access differ between metropolitan and nonmetropolitan (rural) areas?  
3. Which specific counties represent the most critical *"healthcare deserts"* that require immediate attention?

---

## Key Features

- **Automated ETL Pipeline:** Scripts automatically fetch, clean, and merge data from multiple sources, creating a unified and analysis-ready dataset.
- **Interactive Geospatial Map:** A dynamic Folium map visualizes healthcare access rates per county, highlights counties with zero facilities, and plots the exact location of each health center.
- **Dynamic Web Dashboard:** A user-friendly Streamlit application allows for deep-dive analysis with interactive filters, sortable data tables, and comparative charts.
- **Data-Driven Segmentation:** Counties are classified as "Metropolitan" or "Nonmetropolitan" using USDA Rural-Urban Continuum Codes, enabling targeted analysis of rural healthcare gaps.

---

## Technologies Used

- **Data Manipulation & Analysis:** Python, Pandas, GeoPandas  
- **Data Acquisition:** Requests (for Census API), python-dotenv  
- **Data Visualization:** Streamlit, Plotly, Folium  
- **Version Control:** Git, GitHub  

---

## Project Pipeline

The project is executed through a series of numbered Python scripts located in the `scripts/` directory:

1. `data_from_census.py`: Fetches county-level population data for Georgia from the U.S. Census Bureau API.  
2. `merge_facilities_with_population.py`: Merges the HRSA health center locations with the census population data.  
3. `analyze_county_access.py`: Calculates the key metric "Facilities per 10,000 People" for each county.  
4. `add_rural_urban_codes.py`: Enriches the dataset by adding USDA Rural-Urban Continuum Codes.  
5. `generate_access_map.py`: Generates the interactive `georgia_healthcare_access_map.html` file.  

---


## Local Setup and Execution

To run this project on your local machine, follow these steps:

### 1. Cloning my repository

git clone https://github.com/your-username/healthcare-access-analyzer-ga.git
cd healthcare-access-analyzer-ga

### 2. Set Up a Virtual Environment (Recommended)

python -m venv venv
source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set Up Environment Variables

- Get a free API key from the U.S. Census Bureau.

- Rename the .env.example file to .env.

- Add your API key to the .env file in this variable:

        CENSUS_API_KEY="YOUR_CENSUS_API_KEY_HERE"

### 5. Download Required Data

- Download the Health Center Service Delivery Sites CSV and save it in the project root as "Health_Center_Service_Delivery_and_LookAlike_Sites.csv".

- Download the Rural-urban Continuum Codes Excel file and save it in the project root as Ruralurbancontinuumcodes2023.csv.

- Download the TIGER/Line Shapefile for US Counties and extract it into a folder named tl_2022_us_county in the project root.

### 6. Run the Data Pipeline
Execute the scripts in order from the root directory:

python scripts/01_fetch_census_data.py
python scripts/02_merge_facilities_with_population.py
# ... and so on for all scripts

### 7. Launch the Dashboard

Run this command in your directory where the file is: streamlit run dashboard/app.py
Your browser should open to http://localhost:8501 with the interactive dashboard.

## Key Insights
- Significant disparities exist in healthcare access between Georgia's metropolitan and nonmetropolitan counties.

- Several nonmetropolitan counties were identified with zero registered health centers, despite having thousands of residents, making them critical healthcare deserts.

- Counties in the Atlanta metropolitan area show the highest concentration of facilities, but some still exhibit a low facilities-per-capita ratio due to their large populations.