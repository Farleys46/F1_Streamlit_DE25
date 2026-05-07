import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from f1_monza.utils.constants import COMPOUND_COLORS, SEASON_COLORS


def plot_tyre_strategy(stints_df):
    if stints_df.empty:
        return go.Figure().update_layout(title="No data available")

    fig = go.Figure()

    drivers = sorted(stints_df["name_acronym"].unique(), reverse=True)

    # Find the max number of stints
    max_stints = stints_df["stint_number"].max()

    # Loop through each stint number in chronological order, from 1 to max_stints
    for stint_num in range(1, int(max_stints) + 1):
        # Get only the data for this specific stint
        stint_data = stints_df[stints_df["stint_number"] == stint_num]

        if stint_data.empty:
            continue

        # Build a list of colors for these specific drivers
        colors = [COMPOUND_COLORS.get(c, "grey") for c in stint_data["compound"]]

        fig.add_trace(
            go.Bar(
                x=stint_data["stint_length"],
                y=stint_data["name_acronym"],
                orientation="h",
                marker_color=colors,
                name=f"Stint {stint_num}",
                showlegend=False,
                # Added a hover tooltip
                customdata=stint_data["compound"],
                hovertemplate="Driver: %{y}<br>Laps: %{x}<br>Tyre: %{customdata}<extra></extra>",
            )
        )

    # Add a fake legend to show the colors and tyre compounds
    existing_compounds = stints_df["compound"].unique()
    for compound in existing_compounds:
        if compound in COMPOUND_COLORS:
            fig.add_trace(
                go.Bar(
                    x=[None],
                    y=[None],  # Invisible
                    marker_color=COMPOUND_COLORS[compound],
                    name=compound,
                )
            )

    # Layout settings
    fig.update_layout(
        barmode="stack",
        yaxis={"categoryarray": drivers},
        height=700,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=30, b=0),
    )

    # Clean up the axes
    fig.update_xaxes(
        showgrid=True, gridcolor="rgba(128,128,128,0.2)", title="Number of Laps"
    )
    fig.update_yaxes(showgrid=False, title="")

    return fig


def plot_starting_tyres(stints_df):
    if stints_df.empty:
        return go.Figure().update_layout(title="No data available")

    start_stint = stints_df[stints_df["stint_number"] == 1]

    tyre_counts = start_stint["compound"].value_counts().reset_index()
    tyre_counts.columns = ["compound", "count"]

    # The donut chart itself
    fig = px.pie(
        tyre_counts,
        values="count",
        names="compound",
        color="compound",
        hole=0.55,
        color_discrete_map=COMPOUND_COLORS,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="value",
        marker=dict(line=dict(color="#000000", width=1)),
        textfont=dict(color="black", size=15),
    )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig


def plot_air_temp_lollipop(air_temp_data, selected_track):
    """Lollipop chart of average race-day air temp per track and season.

    When 'All' tracks are shown, tracks are ordered by 2025 air temp (hottest first).
    """
    if air_temp_data.empty:
        return go.Figure().update_layout(title="No data available")

    air_temp_data = air_temp_data.copy()

    # When showing all tracks, order them by 2025 temperature (hottest first)
    if selected_track == "All":
        track_order_2025 = (
            air_temp_data[air_temp_data["year"] == 2025]
            .sort_values("air_temperature", ascending=False)["circuit_short_name"]
            .tolist()
        )

        # Tracks that don't appear in 2025 data go at the end
        other_tracks = [
            track
            for track in air_temp_data["circuit_short_name"].unique()
            if track not in track_order_2025
        ]

        track_order = track_order_2025 + other_tracks

        air_temp_data["circuit_short_name"] = pd.Categorical(
            air_temp_data["circuit_short_name"],
            categories=track_order,
            ordered=True,
        )

        air_temp_data = air_temp_data.sort_values(["circuit_short_name", "year"])

    fig = go.Figure()

    # Vertical "stick" lines from y=0 up to the highest temp per track
    highest_temp_per_track = (
        air_temp_data.groupby("circuit_short_name", observed=True)["air_temperature"]
        .max()
        .reset_index()
    )

    for _, row in highest_temp_per_track.iterrows():
        fig.add_shape(
            type="line",
            x0=row["circuit_short_name"],
            x1=row["circuit_short_name"],
            y0=0,
            y1=row["air_temperature"],
            line=dict(color="#666", width=1),
            layer="below",
        )

    # One scatter trace per year (the "lollipop heads")
    for year, year_data in air_temp_data.groupby("year"):
        fig.add_trace(
            go.Scatter(
                x=year_data["circuit_short_name"],
                y=year_data["air_temperature"],
                mode="markers",
                name=str(year),
                marker=dict(
                    color=SEASON_COLORS.get(int(year), "#888"),
                    size=12,
                    line=dict(color="#0D0D0D", width=1),
                ),
                hovertemplate=(
                    "<b>%{x}</b><br>" f"{int(year)}: %{{y:.1f}} °C" "<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        height=420,
        title=dict(text="Seasons' Air Temperature at Tracks", x=0),
        legend=dict(orientation="h", y=1.1, x=0, title=dict(text="Year")),
    )
    fig.update_yaxes(ticksuffix=" °C", range=[0, None])
    fig.update_xaxes(tickangle=-45)

    return fig
