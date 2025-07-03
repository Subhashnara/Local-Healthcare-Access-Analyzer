import streamlit as st
import pandas as pd
import plotly.express as px


county_summary_file_path = 'county_healthcare_summary_GA_with_rucc.csv'

st.set_page_config(layout="wide") # Use wide layout
st.title("🏥 Local Healthcare Access and Wait Time Analyzer: Georgia")
st.write("Analyzing healthcare facility distribution and access across counties in Georgia.")


@st.cache_data 
def load_data(path):
    try:
        df = pd.read_csv(path)
        df['State_FIPS'] = df['State_FIPS'].astype(str)
        df['County_FIPS'] = df['County_FIPS'].astype(str)
        if 'Full_FIPS' in df.columns:
            df['Full_FIPS'] = df['Full_FIPS'].astype(str)
 
        df['Total_Population'] = pd.to_numeric(df['Total_Population'], errors='coerce').fillna(0)
        df['num_facilities'] = pd.to_numeric(df['num_facilities'], errors='coerce').fillna(0)
        df['Facilities_Per_10K_People'] = pd.to_numeric(df['Facilities_Per_10K_People'], errors='coerce').fillna(0)
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{path}' was not found. Please check the file path.")
        return pd.DataFrame() 
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame()

df_county_summary = load_data(county_summary_file_path)

if not df_county_summary.empty:

    st.sidebar.header("Filter Options")


    all_categories = ['All'] + list(df_county_summary['Urban_Rural_Category'].unique())
    selected_category = st.sidebar.selectbox("Filter by Urban/Rural Category", all_categories)


    all_counties = ['All'] + sorted(df_county_summary['County_Name'].unique().tolist())
    selected_county = st.sidebar.selectbox("Select County", all_counties)


    filtered_df = df_county_summary.copy()
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['Urban_Rural_Category'] == selected_category]
    if selected_county != 'All':
        filtered_df = filtered_df[filtered_df['County_Name'] == selected_county]


    st.header("County Healthcare Summary (Filtered)")
    st.write("Browse healthcare access metrics per county, with options to filter by urban/rural category and specific counties.")


    st.dataframe(filtered_df)

    st.markdown("---")


    st.header("Key Metrics for Selected Area")
    if not filtered_df.empty:
        total_pop = filtered_df['Total_Population'].sum()
        total_facilities = filtered_df['num_facilities'].sum()
        avg_facilities_per_10k = filtered_df['Facilities_Per_10K_People'].mean()

        col1, col2, col3 = st.columns(3) 
        with col1:
            st.metric("Total Population", f"{total_pop:,.0f}")
        with col2:
            st.metric("Total Facilities", f"{total_facilities:,.0f}")
        with col3:
            st.metric("Avg. Facilities per 10K People", f"{avg_facilities_per_10k:.2f}")
    else:
        st.info("No data for the current filter selection.")


    st.markdown("---")


    st.header("Urban vs. Rural Healthcare Access Overview")
    urban_rural_analysis = df_county_summary.groupby('Urban_Rural_Category').agg(
        Average_Facilities_Per_10K_People=('Facilities_Per_10K_People', 'mean'),
        Total_Counties=('County_Name', 'count'),
        Total_Facilities=('num_facilities', 'sum'),
        Total_Population=('Total_Population', 'sum')
    ).reset_index()
    
    st.dataframe(urban_rural_analysis)

    st.markdown("---")

    st.header("Top 10 Populous Counties & Facilities")
    top_10_pop_counties = df_county_summary.sort_values(by='Total_Population', ascending=False).head(10)
    fig_pop_fac = px.bar(
        top_10_pop_counties,
        x='County_Name',
        y=['Total_Population', 'num_facilities'],
        title='Total Population and Number of Facilities in Top 10 Most Populous Counties',
        labels={'value': 'Count', 'variable': 'Metric'},
        barmode='group'
    )
    st.plotly_chart(fig_pop_fac, use_container_width=True)

    st.markdown("---") # Separator


    st.header("Top 10 Underserved Nonmetropolitan Counties")
    low_facilities_nonmetro = df_county_summary[
        (df_county_summary['Urban_Rural_Category'] == 'Nonmetropolitan') &
        (df_county_summary['Facilities_Per_10K_People'] < 0.5) & # Using a threshold for "low"
        (df_county_summary['Total_Population'] > 0)
    ].sort_values(by='Facilities_Per_10K_People', ascending=True).head(10) # Top 10 lowest ratios

    if not low_facilities_nonmetro.empty:
        fig_underserved = px.bar(
            low_facilities_nonmetro,
            x='County_Name',
            y='Facilities_Per_10K_People',
            title='Top 10 Underserved Nonmetropolitan Counties (Lowest Facilities per 10K People)',
            labels={'Facilities_Per_10K_People': 'Facilities per 10K People'},
            color='Facilities_Per_10K_People',
            color_continuous_scale=px.colors.sequential.YlOrRd # Red for lower values
        )
        st.plotly_chart(fig_underserved, use_container_width=True)
    else:
        st.info("No nonmetropolitan counties found with low facilities per 10K people based on current criteria.")


else:
    st.warning("No data loaded. Please ensure 'county_healthcare_summary_GA_with_rucc.csv' exists and is accessible.")

st.markdown("---")
st.markdown("Developed as part of the 'Local Healthcare Access and Wait Time Analyzer' project.")