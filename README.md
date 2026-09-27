# Movie Insights — interactive data dashboard

A Streamlit portfolio project for exploring movie ratings, genres and budgets.
All charts, metrics, the table and CSV export use one shared set of filters.

## Run
Requires Python 3.11–3.13.
```sh
python -m venv .venv
# PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run data_analysis.py
```

## Check
```sh
python -m unittest discover -s tests -v
```
Tests cover intersecting filters, the included dataset and Streamlit UI/empty state.

## Walkthrough
Choose genres, a year range and a score range. Compare average budgets,
rating distributions and movie counts, inspect matching rows and export CSV.
An empty selection displays a clear message instead of misleading charts.

## Data decisions and limits
Movies without name/genre/year/score are excluded. Missing budgets are excluded
only from budget averages. Budgets are nominal and not inflation-adjusted.
The included CSV is demonstration data; its original source and redistribution
license still need documentation before broader redistribution. No claim of
business ROI, live data or a publicly hosted deployment is made.

## Structure
- dashboard_data.py: loading, cleaning and shared filters.
- data_analysis.py: presentation.
- tests/: logic and Streamlit application checks.
