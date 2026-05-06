import streamlit as st
import plotly.express as px

from f1_monza.utils.constants import STYLE_PATH
from f1_monza.utils.helpers import get_weather_df, read_css
read_css(STYLE_PATH / "dark.css")

weather_df = get_weather_df()
weather_df["year"] = weather_df["date"].dt.year

st.title("Weather Dashboard")

# KPI--------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average Air Temp", f"{weather_df['air_temperature'].mean():.1f} °C")

with col2:
    st.metric("Average Track Temp", f"{weather_df['track_temperature'].mean():.1f} °C")

with col3:
    st.metric("Average Humidity", f"{weather_df['humidity'].mean():.1f}%")

st.divider()

# Filter------------------------
selected_years = st.multiselect(
    "Select year",
    options=sorted(weather_df["year"].unique()),
    default=sorted(weather_df["year"].unique()),
)

filtered_df = weather_df[weather_df["year"].isin(selected_years)]

# Horizontal bar chart----------
st.subheader("Average Air Temperature by Track")

bar_df = (
    filtered_df
    .groupby("location", as_index=False)["air_temperature"]
    .mean()
    .sort_values("air_temperature", ascending=True)
)

fig_bar = px.bar(
    bar_df,
    x="air_temperature",
    y="location",
    orientation="h",
    color="air_temperature",
    title="Average Air Temperature by Track",
)

fig_bar.update_layout(
    xaxis_title="Average Air Temperature (°C)",
    yaxis_title="Track",
)

st.plotly_chart(fig_bar, width="stretch")

st.divider()

# Bubble chart---------------
st.subheader("Weather Conditions by Track")

bubble_df = (
    filtered_df
    .groupby(["location", "year"], as_index=False)
    .agg({
        "air_temperature": "mean",
        "humidity": "mean",
        "wind_speed": "mean",
    })
)

fig_bubble = px.scatter(
    bubble_df,
    x="humidity",
    y="air_temperature",
    size="wind_speed",
    color="year",
    hover_name="location",
    size_max=45,
    title="Track Weather Conditions",
)

fig_bubble.update_layout(
    xaxis_title="Average Humidity (%)",
    yaxis_title="Average Air Temperature (°C)",
)

st.plotly_chart(fig_bubble, width="stretch")