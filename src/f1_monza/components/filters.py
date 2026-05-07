"""Reusable filter widgets used across multiple pages."""

import streamlit as st

from f1_monza.utils.constants import YEARS


def year_selector(
    label: str = "Season",
    key: str | None = None,
    include_all: bool = False,
    default_index: int = 2,
):
    """Year dropdown - used on tire_strategy and laps pages.

    include_all=True adds "All Years" as the first option.
    key is needed when there are multiple year_selectors on the same page.
    """
    # Add "All Years" first if needed (used on tire_strategy)
    options = (["All Years"] + YEARS) if include_all else YEARS

    return st.selectbox(label, options=options, index=default_index, key=key)


def session_selector(
    label: str = "Session",
    key: str | None = None,
):
    """Qualifying / Race radio button - used on laps page."""
    return st.radio(
        label,
        options=["Qualifying", "Race"],
        horizontal=True,
        key=key,
    )
