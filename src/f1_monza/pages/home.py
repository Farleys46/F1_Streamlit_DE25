import base64
import re
from pathlib import Path

import streamlit as st

from f1_monza.utils.constants import IMAGE_PATH, MARKDOWN_PATH
from f1_monza.utils.helpers import (
    get_drivers_df,
    get_positions_df,
    read_markdown_sections,
    section_header,
)


def _read_svg(path: Path) -> str:
    """Read an SVG and strip its <defs><style> block so Streamlit doesn't render it as code."""
    svg = path.read_text(encoding="utf-8")
    svg = re.sub(r"<defs>.*?</defs>", "", svg, flags=re.DOTALL)
    return svg


def _encode_png(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def _info_card(title: str, value: str, sublabel: str | None = None) -> None:
    sub_html = f'<div class="info-card-sublabel">{sublabel}</div>' if sublabel else ""
    st.markdown(
        f"""
        <div class="info-card">
          <div class="info-card-title">{title}</div>
          <div class="info-card-value">{value}</div>
          {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


SECTOR_COPY = {
    "All sectors": (
        "Monza is the fastest circuit on the F1 calendar — drivers spend roughly 80% of every "
        "lap at full throttle. With long straights and only a handful of slow chicanes, the "
        "cars run extreme low-downforce setups."
    ),
    "Sector 1": (
        "Sector 1 starts on the main straight — the longest flat-out stretch of the season — "
        "and ends after Variante della Roggia. Drivers reach over 350 km/h before braking hard "
        "for Variante del Rettifilo, the tight first chicane where overtakes happen on lap 1."
    ),
    "Sector 2": (
        "Sector 2 winds through the Lesmo curves and the long Curva del Serraglio. Cars stay "
        "above 280 km/h for almost the entire sector, making aerodynamic balance and tyre "
        "temperature management critical."
    ),
    "Sector 3": (
        "Sector 3 includes the second Ascari chicane and the iconic Parabolica — a long "
        "right-hander leading onto the start-finish straight. A clean exit here directly "
        "translates to top speed past the line."
    ),
}


def _track_panel(sector: str) -> None:
    sector_to_file = {
        "All sectors": "track_full.png",
        "Sector 1": "track_sector_1.png",
        "Sector 2": "track_sector_2.png",
        "Sector 3": "track_sector_3.png",
    }
    track_b64 = _encode_png(IMAGE_PATH / sector_to_file[sector])
    st.markdown(
        f"""
        <div class="track-panel">
          <div class="track-eyebrow">Autodromo Nazionale Monza</div>
          <img class="track-img" src="data:image/png;base64,{track_b64}" alt="Monza track" />
          <p class="track-copy">{SECTOR_COPY.get(sector, "")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _get_monza_winners() -> dict[int, tuple[str, str]]:
    positions = get_positions_df()
    drivers = get_drivers_df()

    race_winners = positions[
        (positions["position"] == 1) & (positions["session_type"] == "Race")
    ]

    out: dict[int, tuple[str, str]] = {}
    for year in [2023, 2024, 2025]:
        row = race_winners[race_winners["year"] == year]
        if row.empty:
            continue
        winner_number = int(row["driver_number"].iloc[0])
        session_key = int(row["session_key"].iloc[0])

        drv = drivers[
            (drivers["session_key"] == session_key)
            & (drivers["driver_number"] == winner_number)
        ]
        if drv.empty:
            continue
        out[year] = (
            str(drv["name_acronym"].iloc[0]),
            str(drv["team_name"].iloc[0]),
        )
    return out


def home():
    sections = read_markdown_sections(MARKDOWN_PATH / "home.md")
    monza_title = _read_svg(IMAGE_PATH / "monza_title.svg")
    trackmetrics_logo = _read_svg(IMAGE_PATH / "trackmetrics_logo.svg")

    # ----- Hero -----
    hero_html = (
        '<div class="hero">'
        f'<div class="hero-logo">{trackmetrics_logo}</div>'
        f'<div class="hero-title-wrap">{monza_title}</div>'
        "</div>"
    )
    st.markdown(hero_html, unsafe_allow_html=True)

    # ----- Welcome paragraph -----
    st.markdown(sections["welcome"])

    # ----- Track explorer (tabs for each sector) -----
    section_header("EXPLORE THE TRACK")
    tab_all, tab_s1, tab_s2, tab_s3 = st.tabs(
        ["All sectors", "Sector 1", "Sector 2", "Sector 3"]
    )
    with tab_all:
        _track_panel("All sectors")
    with tab_s1:
        _track_panel("Sector 1")
    with tab_s2:
        _track_panel("Sector 2")
    with tab_s3:
        _track_panel("Sector 3")

    # ----- Monza winners -----
    section_header("ITALIAN GP WINNERS")
    winners = _get_monza_winners()
    win_cols = st.columns(3)
    for col, year in zip(win_cols, [2023, 2024, 2025]):
        with col:
            if year in winners:
                driver, team = winners[year]
                _info_card(str(year), driver, sublabel=team)
            else:
                _info_card(str(year), "—", sublabel="No data")

    # ----- New to F1? -----
    section_header("NEW TO F1?")

    with st.expander("🏁 What's a pit stop?"):
        st.markdown(sections["pit_stop"])

    with st.expander("🛞 What's a stint?"):
        st.markdown(sections["stint"])

    with st.expander("🔴 🟡 ⚪ What are the tyre compounds?"):
        st.markdown(sections["compounds"])

    # ----- About the project -----
    section_header("ABOUT THE PROJECT")
    cols = st.columns(3)
    with cols[0]:
        _info_card(
            "GROUP 2",
            "INDIRA | JULIUS | FILIPPA | FILIP",
            sublabel="Data Engineer '25'",
        )
    with cols[1]:
        _info_card("DATA SOURCE", "OpenF1 API", sublabel="Real-time F1 telemetry")
    with cols[2]:
        _info_card("STACK", "Python · DuckDB", sublabel="Streamlit · Plotly · Power BI")


if __name__ == "__main__":
    home()
