# Geospatial Analysis of Healthcare Accessibility in Georgia

I'm facing some issues with the streamlit dashboards, as of now I'm attaching the screenshots 

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

1. `01_fetch_census_data.py`: Fetches county-level population data for Georgia from the U.S. Census Bureau API.  
2. `02_merge_facilities_with_population.py`: Merges the HRSA health center locations with the census population data.  
3. `03_analyze_county_access.py`: Calculates the key metric "Facilities per 10,000 People" for each county.  
4. `04_add_rural_urban_codes.py`: Enriches the dataset by adding USDA Rural-Urban Continuum Codes.  
5. `05_generate_access_map.py`: Generates the interactive `georgia_healthcare_access_map.html` file.  

---

## Local Setup and Execution

To run this project on your local machine, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/healthcare-access-analyzer-ga.git
cd healthcare-access-analyzer-ga
