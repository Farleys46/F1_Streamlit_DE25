import streamlit as st

st.set_page_config(
    page_title="F1 Monza · Group 2",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded",
)

pages = [
    st.Page("pages/home.py", title="Home", icon="🏁", default=True),
    st.Page("pages/tire_strategy.py", title="Tire Strategy", icon="🛞"),
    st.Page("pages/laps.py", title="Laps", icon="⏱️"),
    st.Page("pages/weather.py", title="Weather", icon="🌤️"),
    st.Page("pages/raw_data.py", title="Raw Data", icon="📊"),
]

pg = st.navigation(pages, position="sidebar")
pg.run()
