import plotly.graph_objects as go
import plotly.express as px
from f1_monza.utils.constants import COMPOUND_COLORS

def plot_tyre_strategy(stints_df):
    if stints_df.empty:
        return go.Figure().update_layout(title="No data available")
    
    fig = go.Figure()
    
    drivers = sorted(stints_df['name_acronym'].unique(), reverse=True)
    
    # Hitta max stints
    max_stints = stints_df['stint_number'].max()
    
    # Loopar över varje stint-nummer i kronologisk ordning, från 1 till max_stints.
    for stint_num in range(1, int(max_stints) + 1):
        # Hämta bara datan för just denna stint
        stint_data = stints_df[stints_df['stint_number'] == stint_num]
        
        if stint_data.empty:
            continue
            
        # Skapa en lista med färger för dessa specifika förare
        colors = [COMPOUND_COLORS.get(c, 'grey') for c in stint_data['compound']]
        
        fig.add_trace(go.Bar(
            x=stint_data['stint_length'],
            y=stint_data['name_acronym'],
            orientation='h',
            marker_color=colors,
            name=f"Stint {stint_num}",
            showlegend=False,
            
            # La till en "hover" funktion
            customdata=stint_data['compound'],
            hovertemplate="Driver: %{y}<br>Laps: %{x}<br>Tyre: %{customdata}<extra></extra>"
        ))

    # Lägg till en fake legend för att visa färgerna och däcktyperna. 
    existing_compounds = stints_df['compound'].unique()
    for compound in existing_compounds:
        if compound in COMPOUND_COLORS:
            fig.add_trace(go.Bar(
                x=[None], y=[None], # Osynlig
                marker_color=COMPOUND_COLORS[compound],
                name=compound
            ))

    # Ändra layout inställningarna
    fig.update_layout(
        barmode="stack",
        yaxis={'categoryarray': drivers}, 
        height=700,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    # Snygga till axlarna
    fig.update_xaxes(showgrid=True, gridcolor="rgba(128,128,128,0.2)", title="Number of Laps")
    fig.update_yaxes(showgrid=False, title="")

    return fig


def plot_starting_tyres(stints_df):
    if stints_df.empty:
        return go.Figure().update_layout(title="No data available")
    
    start_stint = stints_df[stints_df['stint_number'] == 1]
    
    tyre_counts = start_stint['compound'].value_counts().reset_index()
    tyre_counts.columns = ['compound', 'count']
    
    # Själva donut grafen
    
    fig = px.pie(
        tyre_counts,
        values='count',
        names='compound',
        color='compound',
        hole=0.55,
        color_discrete_map=COMPOUND_COLORS
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='value',
        marker=dict(line=dict(color='#000000', width=1)),
        textfont=dict(color='black', size=15)
    )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig