from pathlib import Path

# --- Paths -------------------------------------------------------------------
ASSETS_PATH = Path(__file__).parents[1] / "assets"
DATA_PATH = ASSETS_PATH / "data"
IMAGE_PATH = ASSETS_PATH / "image"
STYLE_PATH = ASSETS_PATH / "style"
MARKDOWN_PATH = ASSETS_PATH / "markdown"

# --- Tyre compound colors (official F1 palette) ------------------------------
COMPOUND_COLORS = {
    "SOFT": "#E10600",
    "MEDIUM": "#FFD800",
    "HARD": "#FFFFFF",
    "INTERMEDIATE": "#43B02A",
    "WET": "#0067AD",
    "UNKNOWN": "#666666",
}

# --- Trackmetrics dark palette ----------------------------------------------
COLORS = {
    "bg": "#0A0A0A",
    "panel": "#111111",
    "border": "#1F1F1F",
    "text": "#FFFFFF",
    "text_dim": "#8A8A8A",
    "accent": "#E10600",  # F1 red
    "accent_2": "#FFD800",  # medium-tyre yellow
}

# --- Season colors (used by weather lollipop chart) -------------------------
SEASON_COLORS = {
    2023: "#3FA9F5",
    2024: "#3FE0A1",
    2025: "#E10600",
}

# --- Years available ---------------------------------------------------------
YEARS = [2023, 2024, 2025]
