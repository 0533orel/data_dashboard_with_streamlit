from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "data" / "movies.csv"

def load_movies(path=DATA_PATH):
    data = pd.read_csv(path)
    required = {"name", "genre", "year", "score", "budget"}
    if not required.issubset(data.columns):
        raise ValueError("Dataset is missing required movie columns")
    for column in ("year", "score", "budget"):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    # A missing budget must not discard a movie from score/count statistics.
    return data.dropna(subset=["name", "genre", "year", "score"]).drop_duplicates()

def filter_movies(data, genres, years, scores):
    return data[
        data["genre"].isin(genres)
        & data["year"].between(*years)
        & data["score"].between(*scores)
    ].copy()
