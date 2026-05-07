import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from f1_monza.utils.helpers import get_weather_df, get_seasons_air_temp


weather_df = get_weather_df()
weather_df["year"] = weather_df["date"].dt.year

st.title("Weather Dashboard")

# Sidebar filter
st.sidebar.markdown("### Air Temperature Chart")
track_options = sorted(get_seasons_air_temp()["circuit_short_name"].unique().tolist())

selected_track = st.sidebar.selectbox(
    "Choose track",
    options=["All", *track_options],
    index=0,
)

# KPI
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Air Temp",
        f"{weather_df['air_temperature'].mean():.1f} °C",
    )

with col2:
    monza_race_weather = weather_df[
        (weather_df["circuit_short_name"] == "Monza")
        & (weather_df["session_name"] == "Race")
    ]

    st.metric(
        "Average Track Temp",
        f"{monza_race_weather['track_temperature'].mean():.1f} °C",
    )

with col3:
    st.metric(
        "Average Humidity",
        f"{weather_df['humidity'].mean():.1f}%",
    )

st.divider()

# Lollipop chart
air_temp_data = get_seasons_air_temp()

if selected_track != "All":
    air_temp_data = air_temp_data[
        air_temp_data["circuit_short_name"] == selected_track
    ]

if air_temp_data.empty:
    st.info("No weather data for this track.")
else:
    if selected_track == "All":
        track_order_2025 = (
            air_temp_data[air_temp_data["year"] == 2025]
            .sort_values("air_temperature", ascending=False)["circuit_short_name"]
            .tolist()
        )

        other_tracks = [
            track
            for track in air_temp_data["circuit_short_name"].unique()
            if track not in track_order_2025
        ]

        track_order = track_order_2025 + other_tracks

        air_temp_data["circuit_short_name"] = pd.Categorical(
            air_temp_data["circuit_short_name"],
            categories=track_order,
            ordered=True,
        )

        air_temp_data = air_temp_data.sort_values(
            ["circuit_short_name", "year"]
        )

    season_colours = {
        2023: "#3FA9F5",
        2024: "#3FE0A1",
        2025: "#E10600",
    }

    fig = go.Figure()

    highest_temp_per_track = (
        air_temp_data.groupby("circuit_short_name", observed=True)["air_temperature"]
        .max()
        .reset_index()
    )

    for _, row in highest_temp_per_track.iterrows():
        fig.add_shape(
            type="line",
            x0=row["circuit_short_name"],
            x1=row["circuit_short_name"],
            y0=0,
            y1=row["air_temperature"],
            line=dict(color="#666", width=1),
            layer="below",
        )

    for year, year_data in air_temp_data.groupby("year"):
        fig.add_trace(
            go.Scatter(
                x=year_data["circuit_short_name"],
                y=year_data["air_temperature"],
                mode="markers",
                name=str(year),
                marker=dict(
                    color=season_colours.get(int(year), "#888"),
                    size=12,
                    line=dict(color="#0D0D0D", width=1),
                ),
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    f"{int(year)}: %{{y:.1f}} °C"
                    "<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        height=420,
        title=dict(text="Seasons' Air Temperature at Tracks", x=0),
        legend=dict(orientation="h", y=1.1, x=0, title=dict(text="Year")),
    )

    fig.update_yaxes(ticksuffix=" °C", range=[0, None])
    fig.update_xaxes(tickangle=-45)

    st.plotly_chart(fig, width="stretch")