import streamlit as st

from f1_monza.utils.constants import STYLE_PATH
from f1_monza.utils.helpers import (
    get_drivers_df,
    get_laps_df,
    get_pits_df,
    get_positions_df,
    get_sessions_df,
    get_stints_df,
    get_weather_df,
    read_css,
)


def raw_data():
    read_css(STYLE_PATH / "dark.css")

    st.markdown(
        '<div class="tm-section-label">DATA EXPLORER</div>',
        unsafe_allow_html=True,
    )
    st.markdown("# Raw Data")
    st.markdown(
        "Every dataset that powers this dashboard. Click a tab to explore. "
        "Sorted, filtered, and downloadable from the toolbar."
    )

    tabs = st.tabs(
        ["STINTS", "PIT STOPS", "DRIVERS", "LAPS", "POSITIONS", "WEATHER", "SESSIONS"]
    )

    with tabs[0]:
        df = get_stints_df()
        st.caption(f"{len(df):,} rows · stints.csv")
        st.dataframe(df, use_container_width=True, height=600)

    with tabs[1]:
        df = get_pits_df()
        st.caption(f"{len(df):,} rows · pit_with_compound.csv")
        st.dataframe(df, use_container_width=True, height=600)

    with tabs[2]:
        df = get_drivers_df()
        st.caption(f"{len(df):,} rows · drivers_clean_updated.csv")
        st.dataframe(df, use_container_width=True, height=600)

    with tabs[3]:
        df = get_laps_df()
        st.caption(f"{len(df):,} rows · laps_clean_updated.csv")
        st.dataframe(df, use_container_width=True, height=600)

    with tabs[4]:
        df = get_positions_df()
        st.caption(f"{len(df):,} rows · final_positions.csv")
        st.dataframe(df, use_container_width=True, height=600)

    with tabs[5]:
        df = get_weather_df()
        st.caption(f"{len(df):,} rows · all_weather_data.csv")
        st.dataframe(df, use_container_width=True, height=600)

    with tabs[6]:
        df = get_sessions_df()
        st.caption(f"{len(df):,} rows · sessions_data.csv")
        st.dataframe(df, use_container_width=True, height=600)


raw_data()
