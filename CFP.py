import streamlit as st
import joblib
import numpy as np
import pandas as pd
import pydeck as pdk
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="NYC Smart Cab Fare System",
    page_icon="🚕",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS Styling
# --------------------------------------------------
st.markdown("""
<style>
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
.fare-card {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    color: white;
    box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    animation: fadeIn 0.6s ease-in-out;
}
.fare-amount {
    font-size: 52px;
    font-weight: bold;
}
.fare-label {
    font-size: 18px;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Loading Model
# --------------------------------------------------
#   model = joblib.load("cab_fare_model.pkl")
import os
model_path = os.path.join(os.path.dirname(__file__), "cab_fare_model.pkl")
model = joblib.load(model_path)
# --------------------------------------------------
# NYC Locations
# --------------------------------------------------
NYC_LOCATIONS = {   
    "Times Square": (40.7580, -73.9855),
    "Central Park": (40.7851, -73.9683),
    "JFK Airport": (40.6413, -73.7781),
    "LaGuardia Airport": (40.7769, -73.8740),
    "Wall Street": (40.7060, -74.0086),
    "Brooklyn Bridge": (40.7061, -73.9969),
    "Empire State Building": (40.7484, -73.9857),
    "Grand Central Station": (40.7527, -73.9772)
}

# --------------------------------------------------
# Haversine Distance
# --------------------------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("🚕 NYC Smart Cab Fare System")
st.caption("Machine Learning + Dynamic Pricing Engine")

st.divider()

# --------------------------------------------------
# Responsive Layout
# --------------------------------------------------
col1, col2, col3 = st.columns([2,2,1])

with col1:
    pickup = st.selectbox("📍 Pickup Location", list(NYC_LOCATIONS.keys()))

with col2:
    dropoff_options = [loc for loc in NYC_LOCATIONS.keys() if loc != pickup]
    dropoff = st.selectbox("🏁 Dropoff Location", dropoff_options)

with col3:
    passengers = st.number_input("👥 Passengers", 1, 6, 1)

weather = st.selectbox(
    "🌦️ Weather Condition",
    ["Sunny ☀️", "Rainy 🌧️", "Stormy ⛈️"]
)

# --------------------------------------------------
# Coordinates
# --------------------------------------------------
p_lat, p_lon = NYC_LOCATIONS[pickup]
d_lat, d_lon = NYC_LOCATIONS[dropoff]

distance = haversine(p_lat, p_lon, d_lat, d_lon)

# Dynamic Zoom
zoom_level = 12 if distance < 5 else 10

# --------------------------------------------------
# Route Map (PyDeck)
# --------------------------------------------------
route_points = pd.DataFrame({
    "lat": [p_lat, d_lat],
    "lon": [p_lon, d_lon]
})

path_data = [{
    "path": [[p_lon, p_lat], [d_lon, d_lat]]
}]

line_layer = pdk.Layer(
    "PathLayer",
    data=path_data,
    get_path="path",
    get_color=[0, 128, 255],
    width_scale=20,
    width_min_pixels=4
)

marker_layer = pdk.Layer(
    "ScatterplotLayer",
    data=route_points,
    get_position="[lon, lat]",
    get_color=[255, 0, 0],
    get_radius=200
)

view_state = pdk.ViewState(
    latitude=(p_lat + d_lat) / 2,
    longitude=(p_lon + d_lon) / 2,
    zoom=zoom_level
)

st.pydeck_chart(pdk.Deck(
    layers=[line_layer, marker_layer],
    initial_view_state=view_state
))

st.divider()

# --------------------------------------------------
# Auto Prediction (Reactive)
# --------------------------------------------------
if pickup and dropoff:

    hour = datetime.now().hour

    features = np.array([[
        p_lat,
        p_lon,
        d_lat,
        d_lon,
        passengers,
        distance,
        hour
    ]])

    base_fare = model.predict(features)[0]

    # Minimum Fare
    if base_fare < 3.0:
        base_fare = 3.0

    # Night Charge
    night_charge = 2.5 if (hour >= 20 or hour <= 6) else 0

    # Surge
    surge_multiplier = 1.2 if (16 <= hour <= 19) else 1

    # Weather
    if "Rainy" in weather:
        weather_multiplier = 1.15
    elif "Stormy" in weather:
        weather_multiplier = 1.25
    else:
        weather_multiplier = 1

    # Extra Business Logic
    booking_fee = 1.5
    passenger_charge = passengers * 0.5

    final_fare = ((base_fare + night_charge + booking_fee + passenger_charge)
                  * surge_multiplier * weather_multiplier)

    # --------------------------------------------------
    # Premium Fare Card
    # --------------------------------------------------
    st.markdown(f"""
    <div class="fare-card">
        <div class="fare-label">Final Estimated Fare</div>
        <div class="fare-amount">${round(final_fare,1)}</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("### 📊 Fare Breakdown")

    colA, colB = st.columns(2)

    with colA:
        st.metric("Base Prediction", f"${round(base_fare,1)}")
        st.metric("Distance (KM)", f"{round(distance,1)}")
        st.metric("Booking Fee", f"${booking_fee}")

    with colB:
        st.metric("Night Charge", f"${night_charge}")
        st.metric("Surge Multiplier", f"x{surge_multiplier}")
        st.metric("Weather Multiplier", f"x{weather_multiplier}")