import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st
from geopy.geocoders import Nominatim

st.set_page_config(layout="wide")

# Upload data
st.title("Toronto Dialysis Patient Map")

# Load Excel data (you may need to convert it to .xlsx if it's PDF)
try:
    df = pd.read_excel("For Visual Representation.xls - Sheet1.pdf")
except Exception as e:
    st.error("Couldn't read the file. Try saving it as .xlsx in Excel or Google Sheets.")
    st.stop()

st.write("Raw Data Preview:", df.head())

# Geocode Postal Codes
geolocator = Nominatim(user_agent="geoapi")

def get_lat_lon(postal_code):
    try:
        location = geolocator.geocode(f"{postal_code}, Toronto, Canada")
        if location:
            return pd.Series([location.latitude, location.longitude])
    except:
        return pd.Series([None, None])

if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
    df[['Latitude', 'Longitude']] = df['Postal Code'].apply(get_lat_lon)
    df = df.dropna(subset=["Latitude", "Longitude"])
    df.to_csv("processed_patients.csv", index=False)
else:
    df = pd.read_csv("processed_patients.csv")

# Show Map
m = folium.Map(location=[43.6532, -79.3832], zoom_start=11)

for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        popup=f"{row['Sex']}, {row['Postal Code']}",
        color='blue',
        fill=True
    ).add_to(m)

folium_static(m)

