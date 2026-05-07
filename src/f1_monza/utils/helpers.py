from pathlib import Path

import pandas as pd
import streamlit as st

from f1_monza.utils.constants import DATA_PATH


# ---------------------------------------------------------------------------
# Asset helpers
# ---------------------------------------------------------------------------
def read_textfile(path: Path) -> str:
    """Read a markdown / text / svg file as a string."""
    with open(path, encoding="utf-8") as f:
        return f.read()


def read_css(path: Path) -> None:
    """Inject a CSS file into the running Streamlit page."""
    css = read_textfile(path)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


@st.cache_data
def read_markdown_sections(path: Path) -> dict[str, str]:
    """Read a markdown file split into sections by '# section_name' headers.

    Returns a dict of {section_name: section_content}.
    """
    text = read_textfile(path)
    sections: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("# "):
            if current_key is not None:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = line[2:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_key is not None:
        sections[current_key] = "\n".join(current_lines).strip()

    return sections


# ---------------------------------------------------------------------------
# Data loaders — one per CSV, all cached
# ---------------------------------------------------------------------------
@st.cache_data
def get_stints_df() -> pd.DataFrame:
    """Stints (one row per driver-stint) — Monza 2023-2025."""
    return pd.read_csv(DATA_PATH / "stints.csv")


@st.cache_data
def get_pits_df() -> pd.DataFrame:
    """Pit stops with compound info — Monza 2023-2025."""
    df = pd.read_csv(DATA_PATH / "pit_with_compound.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)
    return df


@st.cache_data
def get_drivers_df() -> pd.DataFrame:
    """Drivers per session — Monza 2023-2025."""
    return pd.read_csv(DATA_PATH / "drivers_clean_updated.csv")


@st.cache_data
def get_laps_df() -> pd.DataFrame:
    """Lap data — Monza 2023-2025."""
    df = pd.read_csv(DATA_PATH / "laps_clean_updated.csv")
    df["date_start"] = pd.to_datetime(df["date_start"], errors="coerce", utc=True)
    return df


@st.cache_data
def get_positions_df() -> pd.DataFrame:
    """Final session positions."""
    return pd.read_csv(DATA_PATH / "final_positions.csv")


@st.cache_data
def get_weather_df() -> pd.DataFrame:
    """Weather data across all circuits/sessions (full season)."""
    df = pd.read_csv(DATA_PATH / "all_weather_data.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)
    return df


@st.cache_data
def get_sessions_df() -> pd.DataFrame:
    """Index of all sessions across all circuits."""
    df = pd.read_csv(DATA_PATH / "sessions_data.csv")
    df["date_start"] = pd.to_datetime(df["date_start"], errors="coerce", utc=True)
    df["date_end"] = pd.to_datetime(df["date_end"], errors="coerce", utc=True)
    return df


# ---------------------------------------------------------------------------
# Aggregations used by views
# ---------------------------------------------------------------------------
@st.cache_data
def get_seasons_air_temp() -> pd.DataFrame:
    """Average race-day air temperature per track and season.

    Used by the lollipop chart on the weather page.
    """
    weather = get_weather_df()

    return (
        weather[weather["session_name"] == "Race"]
        .groupby(["year", "circuit_short_name"], as_index=False)["air_temperature"]
        .mean()
    )


# ---------------------------------------------------------------------------
# Shared UI helpers (used across multiple pages)
# ---------------------------------------------------------------------------
def section_header(text: str) -> None:
    """Red eyebrow text used as a section divider on every page."""
    st.markdown(
        f'<div class="section-header">{text}</div>',
        unsafe_allow_html=True,
    )


@st.cache_data
def get_driver_abbr_map() -> dict[int, str]:
    """Map driver_number -> name_acronym, built from drivers data.

    Used wherever we need to display a driver's 3-letter code.
    """
    drivers = get_drivers_df()
    return (
        drivers.drop_duplicates("driver_number")
        .set_index("driver_number")["name_acronym"]
        .to_dict()
    )
