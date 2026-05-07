import streamlit as st
import pandas as pd


def display_fastest_pit_duration(df):
    if df.empty or "lane_duration" not in df.columns:
        st.metric(label="Fastest Pit Duration", value="Missing data")
        return

    # Find the row with the shortest pit duration
    fastest_pit_duration = df.loc[df["lane_duration"].idxmin()]

    # Values to show in the KPI
    time = fastest_pit_duration["lane_duration"]
    driver = fastest_pit_duration["name_acronym"]
    team = fastest_pit_duration["team_name"]

    # The KPI itself
    st.metric(
        label=f"Fastest Pit Duration: ({driver}) ({team})",
        value=f"{time:.2f} s",
    )


def display_weather_kpis(weather_df):
    """Three weather KPIs: avg air temp, avg track temp (Monza race), avg humidity."""
    col1, col2, col3 = st.columns(3)

    # Average air temperature across all sessions
    with col1:
        st.metric(
            "Average Air Temp",
            f"{weather_df['air_temperature'].mean():.1f} °C",
        )

    # Average track temperature - filtered to Monza race sessions only
    with col2:
        monza_race_weather = weather_df[
            (weather_df["circuit_short_name"] == "Monza")
            & (weather_df["session_name"] == "Race")
        ]
        st.metric(
            "Average Track Temp",
            f"{monza_race_weather['track_temperature'].mean():.1f} °C",
        )

    # Average humidity across all sessions
    with col3:
        st.metric(
            "Average Humidity",
            f"{weather_df['humidity'].mean():.1f}%",
        )
