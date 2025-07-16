import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st
from geopy.geocoders import Nominatim

# Load Excel sheet
df = pd.read_excel("For Visual Representation.xls - Sheet1.pdf")

# Clean and preview data
st.write("Original Data", df.head())

# Convert postal codes to latitude and longitude
geolocator = Nominatim(user_agent="toronto_map")

def get_lat_lon(postal_code):
    try:
        location = geolocator.geocode(f"{postal_code}, Toronto, Canada")
        if location:
            return pd.Series([location.latitude, location.longitude])
    except:
        return pd.Series([None, None])

# Only run geocoding if lat/lon not already there
if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
    df[['Latitude', 'Longitude']] = df['Postal Code'].apply(get_lat_lon)
    df.to_csv("processed_patients.csv", index=False)
else:
    df = pd.read_csv("processed_patients.csv")

# Base Map Centered on Toronto
center = [43.6532, -79.3832]
m = folium.Map(location=center, zoom_start=11)

# Add data points
for _, row in df.iterrows():
    if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            popup=f"{row['Sex']}, {row['Postal Code']}",
            color='blue',
            fill=True
        ).add_to(m)

# Display the map in Streamlit
st.title("Toronto Dialysis Patient Map")
folium_static(m)


pip install pandas streamlit folium geopy streamlit-folium
streamlit run app.py

