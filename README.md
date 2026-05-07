# F1 — Trackmetrics🏁

Data visualization project for the **Data Engineering '25'**
Group 2 — built together with the UX team.

The project explores Formula 1 data from the **Autodromo Nazionale Monza** circuit
across the 2023, 2024 and 2025 seasons. Data comes from the
[OpenF1 API](https://openf1.org/).

---

## What's in here

A multi-page Streamlit dashboard with five views:

- **Home** — intro to the project, the Monza track, and a glossary for people new to F1
- **Tyre Strategy** — pit stops, starting compounds, full-race strategy timeline
- **Laps** — gap-to-fastest bar chart per session and sector, with KPIs
- **Weather** — air/track temperature and humidity across tracks and seasons
- **Raw Data** — every CSV that powers the dashboard, browsable in tabs

A Power BI dashboard with the same data is also part of the project (not in this repo).

---

## How the team is split

The four of us divided the work by domain:

| Person  | Domain                   |
| ------- | ------------------------ |
| Indira  | Home page, raw data page |
| Julius  | Laps & sector times      |
| Filip   | Tyre strategy page       |
| Filippa | Weather                  |

---

## Tech stack

- **Python 3.13**
- **pandas** + **DuckDB** for data wrangling
- **Streamlit** for the dashboard
- **Plotly** for interactive charts
- **uv** for dependency management

---

## Project structure

```
F1_STREAMLIT_DE25/
└── src/f1_monza/
    ├── app.py                   # entry point, st.navigation()
    ├── assets/
    │   ├── data/                # CSVs
    │   ├── image/               # track images, logos
    │   ├── markdown/            # text content for the home page
    │   └── style/               # dashboard.css
    ├── components/
    │   ├── filters.py           # reusable year_selector, session_selector
    │   ├── kpis.py              # reusable KPI components
    │   └── visualizations.py    # all Plotly chart functions
    ├── pages/
    │   ├── home.py
    │   ├── tire_strategy.py
    │   ├── laps.py
    │   ├── weather.py
    │   └── raw_data.py
    └── utils/
        ├── constants.py         # paths, color palettes, year list
        └── helpers.py           # data loaders + shared UI helpers
```

The split between `pages/`, `components/` and `utils/` keeps things DRY:
charts live in `components/visualizations.py`, KPIs in `components/kpis.py`,
shared filters in `components/filters.py`, and pages just glue them together.

## Deliverables checklist

**VG-level:**

- [x] Streamlit dashboard with KPIs, filters, line and bar charts
- [x] DRY, well-structured code
- [x] Power BI follows good design principles
- [x] Streamlit dashboard deployed

---

## Credits

Data: [OpenF1 API](https://openf1.org/) — free, real-time and historical F1 data.
Track image based on the official Monza circuit layout.
Built as a school project, not affiliated with Formula 1, FIA, or any team.
