import streamlit as st
import plotly.express as px
from dashboard_data import load_movies, filter_movies

st.set_page_config(page_title="Movie Insights", layout="wide")
st.title("Movie Insights")
st.caption("Explore movie ratings and budgets. Every chart uses the same sidebar filters.")

@st.cache_data
def cached_movies():
    return load_movies()

try:
    data = cached_movies()
except (OSError, ValueError) as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()

if data.empty:
    st.info("The dataset contains no usable movies.")
    st.stop()

genres = st.sidebar.multiselect("Genres", sorted(data["genre"].unique()), default=sorted(data["genre"].unique()))
minimum, maximum = int(data["year"].min()), int(data["year"].max())
years = st.sidebar.slider("Year range", minimum, maximum, (minimum, maximum)) if minimum < maximum else (minimum, maximum)
scores = st.sidebar.slider("Score range", 0.0, 10.0, (0.0, 10.0), 0.1)
filtered = filter_movies(data, genres, years, scores)

if filtered.empty:
    st.info("No movies match these filters. Select a genre or widen the ranges.")
    st.stop()

a, b, c = st.columns(3)
a.metric("Movies", len(filtered))
b.metric("Average score", f"{filtered['score'].mean():.2f}")
budget = filtered["budget"].mean()
c.metric("Average budget", "Not available" if filtered["budget"].notna().sum() == 0 else f"${budget:,.0f}")
st.caption("Average budgets exclude missing values. Counts and ratings retain those movies.")

left, right = st.columns(2)
with left:
    by_genre = filtered.groupby("genre", as_index=False)["budget"].mean().dropna()
    st.plotly_chart(px.bar(by_genre, x="genre", y="budget", title="Average budget by genre"), use_container_width=True)
    st.plotly_chart(px.histogram(filtered, x="score", nbins=20, title="Score distribution"), use_container_width=True)
with right:
    by_year = filtered.groupby("year", as_index=False)["budget"].mean().dropna()
    st.plotly_chart(px.line(by_year, x="year", y="budget", title="Average budget by year"), use_container_width=True)
    counts = filtered.groupby("genre").size().reset_index(name="movies")
    st.plotly_chart(px.bar(counts, x="genre", y="movies", title="Movies by genre"), use_container_width=True)
st.dataframe(filtered, hide_index=True, use_container_width=True)
st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"), "filtered-movies.csv", "text/csv")
