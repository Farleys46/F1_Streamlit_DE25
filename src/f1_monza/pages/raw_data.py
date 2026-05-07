import streamlit as st

from f1_monza.utils.helpers import (
    get_drivers_df,
    get_laps_df,
    get_pits_df,
    get_positions_df,
    get_sessions_df,
    get_stints_df,
    get_weather_df,
    section_header,
)

# (label, loader function, source filename)
DATASETS = [
    ("STINTS", get_stints_df, "stints.csv"),
    ("PIT STOPS", get_pits_df, "pit_with_compound.csv"),
    ("DRIVERS", get_drivers_df, "drivers_clean_updated.csv"),
    ("LAPS", get_laps_df, "laps_clean_updated.csv"),
    ("POSITIONS", get_positions_df, "final_positions.csv"),
    ("WEATHER", get_weather_df, "all_weather_data.csv"),
    ("SESSIONS", get_sessions_df, "sessions_data.csv"),
]


def raw_data():
    section_header("DATA EXPLORER")
    st.markdown("# Raw Data")
    st.markdown(
        "Every dataset that powers this dashboard. Click a tab to explore. "
        "Sorted, filtered, and downloadable from the toolbar."
    )

    tabs = st.tabs([label for label, _, _ in DATASETS])
    for tab, (_, loader, filename) in zip(tabs, DATASETS):
        with tab:
            df = loader()
            st.caption(f"{len(df):,} rows · {filename}")
            st.dataframe(df, width="stretch", height=600)


if __name__ == "__main__":
    raw_data()
