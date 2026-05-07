import streamlit as st

from f1_monza.utils.helpers import get_pits_df, get_stints_df
from f1_monza.components.filters import year_selector
from f1_monza.components.visualizations import plot_tyre_strategy, plot_starting_tyres
from f1_monza.components.kpis import display_fastest_pit_duration

# Title and quick intro
st.title("Tyre Strategy & Pit Stops")
st.markdown("Analysis of tyre strategy and pit stops during the Monza Grand Prix.")

# Load data
pit_df = get_pits_df()
stints_df = get_stints_df()

col1, col2 = st.columns([1, 3])

# Left side (col1 - 1/3 width)
with col1:
    # Filter
    selected_kpi_year = year_selector(
        label="Select Season:",
        key="kpi_year",
        include_all=True,
        default_index=0,  # default to "All Years"
    )

    # Filter the data for the KPI
    if selected_kpi_year != "All Years":
        filtered_pit_df = pit_df[pit_df["year"] == selected_kpi_year]
        filtered_start_stints_df = stints_df[stints_df["year"] == selected_kpi_year]
    else:
        filtered_pit_df = pit_df
        filtered_start_stints_df = stints_df

    # Draw KPI in col1
    st.markdown("<br>", unsafe_allow_html=True)  # Adds a bit of empty space
    st.subheader("Fastest Pit stop")
    display_fastest_pit_duration(filtered_pit_df)

    # Donut chart
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Drivers' Starting Tyres")
    starting_fig = plot_starting_tyres(filtered_start_stints_df)
    st.plotly_chart(starting_fig, use_container_width=True)


# Right side (col2 - 2/3 width)
with col2:
    # Filter
    selected_chart_year = year_selector(
        label="Select Season for Chart:",
        key="chart_year",
    )

    # Filter the data for the chart
    filtered_stints_df = stints_df[stints_df["year"] == selected_chart_year]

    # Draw the chart in col2
    st.subheader("Tyre Strategy")
    strategy_fig = plot_tyre_strategy(filtered_stints_df)
    st.plotly_chart(strategy_fig, use_container_width=True)
