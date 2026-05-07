import streamlit as st

from f1_monza.utils.helpers import get_pits_df, get_stints_df, read_css
from f1_monza.utils.constants import YEARS, STYLE_PATH

from f1_monza.components.visualizations import plot_tyre_strategy, plot_starting_tyres
from f1_monza.components.kpis import display_fastest_pit_duration

# Läs in css stylingen

read_css(STYLE_PATH / "dashboard.css")


# Rubrik o snabb info etc. 

st.title("Tyre Strategy & Pit Stops")
st.markdown("Analysis of tyre strategy and pit stops during the Monza Grand Prix.")

# Ladda in data

pit_df = get_pits_df()
stints_df = get_stints_df()

col1, col2 = st.columns([1, 3])

# Vänster sida (col1 - 1/3 bredd)
with col1:
    # Filtret
    selected_kpi_year = st.selectbox(
        "Select Season:",
        options=["All Years"] + YEARS
    )

    # Filtrera datan just för KPI:n
    if selected_kpi_year != "All Years":
        filtered_pit_df = pit_df[pit_df['year'] == selected_kpi_year]
        filtered_start_stints_df = stints_df[stints_df['year'] == selected_kpi_year]
    else:
        filtered_pit_df = pit_df
        filtered_start_stints_df = stints_df

    # Rita Kpi i col1
    st.markdown("<br>", unsafe_allow_html=True) # Lägger till lite tomt utrymme
    st.subheader("Fastest Pit stop")
    display_fastest_pit_duration(filtered_pit_df)
    
    #Donut charten
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Drivers' Starting Tyres")
    starting_fig = plot_starting_tyres(filtered_start_stints_df)
    st.plotly_chart(starting_fig, use_container_width=True)


# Höger sida (col2 - 2/3 bredd)
with col2:
    # Filtret
    selected_chart_year = st.selectbox(
        "Select Season for Chart:",
        options=YEARS
    )

    # Filtrera datan just för grafen
    filtered_stints_df = stints_df[stints_df['year'] == selected_chart_year]

    # Rita grafen i col2 
    #st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Tyre Strategy")
    strategy_fig = plot_tyre_strategy(filtered_stints_df)
    st.plotly_chart(strategy_fig, use_container_width=True)
    
    
    
    