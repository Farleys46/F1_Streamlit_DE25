import streamlit as st

from f1_monza.utils.helpers import get_weather_df, get_seasons_air_temp
from f1_monza.components.kpis import display_weather_kpis
from f1_monza.components.visualizations import plot_air_temp_lollipop


def show():
    st.title("Weather Dashboard")

    weather_df = get_weather_df()
    weather_df["year"] = weather_df["date"].dt.year

    # KPIs
    display_weather_kpis(weather_df)

    st.divider()

    # Filter (in main page area to match other pages)
    air_temp_data = get_seasons_air_temp()
    track_options = sorted(air_temp_data["circuit_short_name"].unique().tolist())

    selected_track = st.selectbox(
        "Choose track",
        options=["All", *track_options],
        index=0,
        key="weather_track",
    )

    # Filter data based on track choice
    if selected_track != "All":
        air_temp_data = air_temp_data[
            air_temp_data["circuit_short_name"] == selected_track
        ]

    # Render the chart
    if air_temp_data.empty:
        st.info("No weather data for this track.")
        return

    fig = plot_air_temp_lollipop(air_temp_data, selected_track)
    st.plotly_chart(fig, width="stretch")


if __name__ == "__main__":
    show()
