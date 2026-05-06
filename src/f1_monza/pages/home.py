import streamlit as st

from f1_monza.utils.constants import IMAGE_PATH, MARKDOWN_PATH, STYLE_PATH
from f1_monza.utils.helpers import inline_svg, read_css, read_textfile


def render_header() -> None:
    """Top header: brand mark left, ITALIAN GP label center, MONZA title right."""
    title_svg = inline_svg(IMAGE_PATH / "Ny_monza_titel.svg")
    header_html = f"""
    <div class="tm-header">
      <div class="tm-header-left">▮ Trackmetrics°</div>
      <div class="tm-header-center">ITALIAN GRAND PRIX</div>
      <div class="tm-header-right">{title_svg}</div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def home():
    read_css(STYLE_PATH / "dark.css")
    render_header()

    # --- Intro -----------------------------------------------------------
    col_intro_l, col_intro_r = st.columns([1, 1])
    with col_intro_l:
        st.image(str(IMAGE_PATH / "Hela_banan.png"), use_container_width=True)
    with col_intro_r:
        st.markdown(read_textfile(MARKDOWN_PATH / "intro_home.md"))

    st.markdown("---")

    # --- Sector breakdown ------------------------------------------------
    st.markdown(
        '<div class="tm-section-label">CIRCUIT BREAKDOWN</div>',
        unsafe_allow_html=True,
    )
    st.markdown("## Autodromo Nazionale Monza")

    sectors = [
        ("Section_1.png", "sector_1.md"),
        ("Section_2.png", "sector_2.md"),
        ("Section_3.png", "sector_3.md"),
    ]
    cols = st.columns(3)
    for col, (img, md) in zip(cols, sectors):
        with col:
            st.image(str(IMAGE_PATH / img), use_container_width=True)
            st.markdown(read_textfile(MARKDOWN_PATH / md))


home()
