import re
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from f1_monza.utils.constants import COLORS, IMAGE_PATH
from f1_monza.utils.helpers import (
    get_driver_abbr_map,
    get_laps_df,
    get_positions_df,
    get_weather_df,
)
from f1_monza.components.filters import year_selector, session_selector


def _read_svg(path: Path) -> str:
    svg = path.read_text(encoding="utf-8")
    svg = re.sub(r"<defs>.*?</defs>", "", svg, flags=re.DOTALL)
    return svg


laps_df = get_laps_df()
positions_df = get_positions_df()
weather_df = get_weather_df()

SECTOR_COL_MAP = {
    "Full lap": "lap_duration",
    "Sector 1": "duration_sector_1",
    "Sector 2": "duration_sector_2",
    "Sector 3": "duration_sector_3",
}


def format_gap(seconds: float) -> str:
    return f"+{seconds:.3f}"


def format_laptime(seconds: float) -> str:
    mins = int(seconds // 60)
    secs = seconds % 60
    return f"{mins}:{secs:06.3f}"


def clean_laps(df):
    return df[
        (df["is_pit_out_lap"] == False)
        & (df["lap_duration"].notna())
        & (df["lap_duration"] > 60)
    ].copy()


def get_session_keys(positions_df, year, session_type):
    return positions_df[
        (positions_df["year"] == year) & (positions_df["session_type"] == session_type)
    ]["session_key"].unique()


# Kpi:s
def show_kpis(year, session_type):
    session_key = get_session_keys(positions_df, year, session_type)

    laps_session = laps_df[laps_df["session_key"].isin(session_key)]
    weather_session = weather_df[weather_df["session_key"].isin(session_key)]

    total_laps = laps_session["lap_number"].max()
    avg_track_temp = weather_session["track_temperature"].mean()
    top_speed = laps_session["st_speed"].max()
    avg_lap = clean_laps(laps_session)["lap_duration"].mean()

    col_laps, col_temp, col_speed, col_avg_lap = st.columns(4)
    col_laps.metric("Laps", f"{int(total_laps)}")
    col_temp.metric("Avg Track Temp", f"{avg_track_temp:.2f} °C")
    col_speed.metric("Top Speed", f"{int(top_speed)} Km/h")
    col_avg_lap.metric("Avg Lap Time", format_laptime(float(avg_lap)))


### Barchart ###
def build_gap_chart(year, session_type, sector):
    session_keys = get_session_keys(positions_df, year, session_type)

    pos_filtered = positions_df[
        (positions_df["year"] == year) & (positions_df["session_type"] == session_type)
    ].copy()

    if pos_filtered.empty:
        return None

    laps_session = clean_laps(laps_df)
    laps_session = laps_session[laps_session["session_key"].isin(session_keys)]

    col = SECTOR_COL_MAP[sector]
    sector_laps = laps_session[laps_session[col].notna()]
    best_laps = (
        sector_laps.groupby("driver_number")[col]
        .min()
        .reset_index()
        .rename(columns={col: "best_lap"})
    )
    merged = pos_filtered.merge(best_laps, on="driver_number", how="left")
    merged = merged.dropna(subset=["best_lap"])
    merged = merged.sort_values("best_lap")

    if merged.empty:
        return None

    fastest = merged["best_lap"].min()
    merged["gap"] = merged["best_lap"] - fastest

    abbr_map = get_driver_abbr_map()
    merged["abbr"] = (
        merged["driver_number"]
        .map(abbr_map)
        .fillna(merged["driver_number"].astype(str))
    )
    merged["y_label"] = merged.apply(
        lambda r: f"P{str(r['position']).zfill(2)}. {r['abbr']}", axis=1
    )

    text_labels = [
        format_laptime(row["best_lap"]) if row["gap"] == 0 else format_gap(row["gap"])
        for _, row in merged.iterrows()
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=merged["gap"],
            y=merged["y_label"],
            orientation="h",
            text=text_labels,
            textposition="outside",
            textfont=dict(color=COLORS["text"], size=12, family="monospace"),
            marker=dict(color=COLORS["text"]),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Best lap-time: %{customdata}<br>"
                "Gap: %{text}<extra></extra>"
            ),
            customdata=[format_laptime(v) for v in merged["best_lap"]],
        )
    )

    fig.update_layout(
        plot_bgcolor=COLORS["bg"],
        paper_bgcolor=COLORS["bg"],
        font=dict(color=COLORS["text"], family="monospace"),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(color=COLORS["text_dim"], size=11),
            range=[0, merged["gap"].max() * 1.35],
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(color=COLORS["text"], size=12),
            showgrid=False,
        ),
        margin=dict(l=10, r=80, t=10, b=30),
        height=580,
        bargap=0.35,
        showlegend=False,
    )

    return fig


def show():
    # --- Hero header ---
    monza_title = _read_svg(IMAGE_PATH / "monza_title.svg")
    trackmetrics_logo = _read_svg(IMAGE_PATH / "trackmetrics_logo.svg")

    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-logo">{trackmetrics_logo}</div>
          <div class="hero-title-wrap">{monza_title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Slicers
    col_year, col_session, col_sector = st.columns(3)

    with col_year:
        year = year_selector(label="Year", key="laps_year")

    with col_session:
        session_type = session_selector(key="laps_session")

    with col_sector:
        sector = st.selectbox(
            "Sector",
            options=list(SECTOR_COL_MAP.keys()),
            index=0,
        )

    show_kpis(year, session_type)

    fig = build_gap_chart(year, session_type, sector)

    if fig is None:
        st.warning(f"No data found for {year} - {session_type} - {sector}.")
        return

    st.plotly_chart(fig, width="stretch")


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Laps – Monza")
    show()
