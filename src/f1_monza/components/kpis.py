import streamlit as st
import pandas as pd


def display_fastest_pit_duration(df):
    if df.empty or 'lane_duration' not in df.columns:
        st.metric(label="Fastest Pit Duration", value="Missing data")
        return
    
    # Kortaste pit duration tiden:
    
    fastest_pit_duration = df.loc[df['lane_duration'].idxmin()]
    
    # Vilka värden som ska visas i KPI:n:
    time = fastest_pit_duration['lane_duration']
    driver = fastest_pit_duration['name_acronym']
    team = fastest_pit_duration['team_name']
    
    #Själva KPI:n:
    st.metric(
        label=f"Fastest Pit Duration: ({driver}) ({team})",
        value=f"{time:.2f} s",
    )