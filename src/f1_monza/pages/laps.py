import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "assets" / "data"

DRIVER_ABBR = {
    1: "VER", 4: "NOR", 81: "PIA", 16: "LEC", 63: "RUS",
    44: "HAM", 55: "SAI", 14: "ALO", 11: "PER", 23: "ALB",
    22: "TSU", 3: "RIC", 2: "SAR", 20: "MAG", 31: "OCO",
    10: "GAS", 18: "STR", 27: "HUL", 77: "BOT", 24: "ZHO",
    40: "LAW", 43: "COL", 30: "HAD", 6: "HAD", 12: "ANT",
    5: "BEA", 87: "BOR",
}

def format_gap(seconds: float) -> str:
    return f"+{seconds:.3f}"

def format_laptime(seconds: float) -> str:
    mins = int(seconds //60)
    secs = seconds % 60
    return f"{mins}:{secs:06.3f}"

def clean_laps(laps_df: pd.DataFrame) -> pd.DataFrame:
    return laps_df[
        (laps_df["is_pit_out_lap"] == False) &
        (laps_df["lap_duration"].notna()) &
        (laps_df["lap_duration"] > 60)
    ].copy()

@st.cache_data
def load_data():
    laps = pd.read_csv(DATA_DIR / "laps_clean_updated.csv")
    positions = pd.read_csv(DATA_DIR / "final_positions.csv")
    weather = pd.read_csv(DATA_DIR / "all_weather_data.csv")
    return laps, positions, weather

# Kpi:s
def show_kpis(laps_df, weather_df, positions_df, year, session_type):
    pos_filterd =positions_df[
        (positions_df["year"] == year) & 
        (positions_df["session_type"] == session_type)
    ]
    session_key = pos_filterd["session_key"].unique()

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
def build_gap_chart(
        laps_df: pd.DataFrame,
        positions_df: pd.DataFrame,
        year: int,
        session_type: str,
        sector: str,
) -> go.Figure:
    
    pos_filtered = positions_df[
        (positions_df["year"] == year) &
        (positions_df["session_type"] == session_type)
    ].copy()

    if pos_filtered.empty:
        return None
    
    filtered_laps = clean_laps(laps_df)

    session_keys = pos_filtered["session_key"].unique()
    laps_session = filtered_laps[filtered_laps["session_key"].isin(session_keys)]

    sector_col_map = {
        "Full lap": "lap_duration",
        "Sector 1": "duration_sector_1",
        "Sector 2": "duration_sector_2",
        "Sector 3": "duration_sector_3",
    }
    col = sector_col_map[sector]

    sector_laps = laps_session[laps_session[col].notna()]
    best_laps = (
        sector_laps
        .groupby("driver_number")[col]
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
    merged["abbr"] = merged["driver_number"].map(DRIVER_ABBR).fillna(
        merged["driver_number"].astype(str)
    )

    merged["y_label"] = merged.apply(
        lambda r: f"P{str(r['position']).zfill(2)}. {r['abbr']}", axis=1
    )

    text_labels = []
    for _, row in merged.iterrows():
        if row["gap"] == 0:
            text_labels.append(format_laptime(row["best_lap"]))
        else:
            text_labels.append(format_gap(row["gap"]))
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=merged["gap"],
        y=merged["y_label"],
        orientation="h",
        text=text_labels,
        textposition="outside",
        textfont=dict(color="white", size=12, family="monospace"),
        marker=dict(color="white"),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Best lap-time: %{customdata}<br>"
            "Gap: %{text}<extra></extra>"
        ),
        customdata=[format_laptime(v) for v in merged["best_lap"]],
    ))

    fig.update_layout(
        plot_bgcolor="#0a0a0a",
        paper_bgcolor="#0a0a0a",
        font=dict(color="white", family="monospace"),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="#888888", size=11),
            range=[0, merged["gap"].max() * 1.35],
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(color="white", size=12),
            showgrid=False,
        ),
        margin=dict(l=10, r=80, t=10, b=30),
        height=580,
        bargap=0.35,
        showlegend=False,
    )

    return fig

def show():
    laps_df, positions_df, weather_df = load_data()
    
    # Slicers
    col_year, col_session, col_sector = st.columns(3)

    with col_year:
        year = st.selectbox("Year", options=[2023, 2024, 2025], index=2)

    with col_session:
        session_type = st.radio(
            "Session",
            options=["Qualifying", "Race"],
            horizontal=True,
        )
    
    with col_sector:
        sector = st.selectbox(
            "Sector",
            options=["Full lap", "Sector 1", "Sector 2", "Sector 3"],
            index=0,
        )

    show_kpis(laps_df, weather_df, positions_df, year, session_type)

    fig = build_gap_chart(laps_df, positions_df, year, session_type, sector)

    if fig is None:
        st.warning(f"No data found for {year} - {session_type} - {sector}.")
        return

    st.plotly_chart(fig, width="stretch")

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Laps – Monza")
    show()