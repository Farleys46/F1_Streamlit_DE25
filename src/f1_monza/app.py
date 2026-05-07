import streamlit as st

from f1_monza.utils.constants import STYLE_PATH
from f1_monza.utils.helpers import read_css

st.set_page_config(
    page_title="F1 Monza · Group 2",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject global CSS once — applies to every page
read_css(STYLE_PATH / "dashboard.css")

pages = [
    st.Page("pages/home.py", title="Home", icon="🏁", default=True),
    st.Page("pages/tire_strategy.py", title="Tire Strategy", icon="🛞"),
    st.Page("pages/laps.py", title="Laps", icon="⏱️"),
    st.Page("pages/weather.py", title="Weather", icon="🌤️"),
    st.Page("pages/raw_data.py", title="Raw Data", icon="📊"),
]

pg = st.navigation(pages, position="sidebar")
pg.run()
