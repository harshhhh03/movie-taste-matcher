import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import random

# ---- DATASET ----
movies_data = {
    'Inception':      [5, 1, 5, 2, 0],
    'Barbie':         [1, 5, 0, 5, 2],
    'Oppenheimer':    [5, 2, 5, 1, 5],
    'Dune: Part Two': [5, 1, 4, 0, 0],
    'The Godfather':  [2, 5, 4, 0, 5],
    'Pulp Fiction':   [0, 5, 4, 1, 5],
    'Super Mario':    [1, 5, 1, 5, 1]
}

users = ['You', 'Alex', 'Beth', 'Charlie', 'David']
df = pd.DataFrame(movies_data, index=users)

# ---- POSTER LINKS ----
poster_links = {
    "Inception": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
    "Barbie":   "https://image.tmdb.org/t/p/w500/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg",
    "Oppenheimer": "https://image.tmdb.org/t/p/w500/5pT8t04F93as1Z6Yy9kVbpQEwXg.jpg",
    "Dune: Part Two": "https://image.tmdb.org/t/p/w500/8b8R8l88Qje9dn9OE8PY05Nxl1X.jpg",
    "The Godfather": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
    "Pulp Fiction": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
    "Super Mario": "https://image.tmdb.org/t/p/w500/qNBAXBIQlnOThrVvA6mA2B5ggV6.jpg"
}

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Movie Taste Matcher", layout="wide")

# ---- CUSTOM CSS ----
st.markdown("""
<style>
.main {background:#0a0a0a; color:white;}
h1, h2, h3 {color:white !important; text-align:center; font-family:Poppins;}

.movie-row {
    display:flex;
    justify-content:center;
    gap:26px;
    padding:14px;
    flex-wrap:wrap;
}
.movie-box {
    background:#111;
    padding:10px;
    border-radius:10px;
    border:1px solid #333;
    width:160px;
    text-align:center;
    transition:0.3s;
}
.movie-box:hover {
    transform:scale(1.08);
    border:1px solid red;
    box-shadow:0 0 12px red;
}
.movie-box img {
    border-radius:6px;
}
</style>
""", unsafe_allow_html=True)

# ---- HEADER / TITLE ----
st.markdown("<h2 class='glow'>🎞 Movie Taste Matcher</h2>", unsafe_allow_html=True)
st.divider()

# ---- SEARCH BAR (NEWLY ADDED) ----
search_movie = st.text_input("🔍 Search a movie", placeholder="Type movie name here...")

if search_movie:
    matched_movies = [m for m in df.columns if search_movie.lower() in m.lower()]
    
    if matched_movies:
        st.markdown("<h3>🎬 Search Results</h3>", unsafe_allow_html=True)
        row = "<div class='movie-row'>"
        for m in matched_movies:
            img = poster_links.get(m, "")
            row += f"""
            <div class='movie-box'>
                <img src='{img}' width='140'>
                <div>{m}</div>
            </div>
            """
        row += "</div>"
        st.markdown(row, unsafe_allow_html=True)
    else:
        st.warning("❌ No movies matched your search")

    st.divider()

# ---- SIDEBAR RATINGS ----
with st.sidebar:
    st.markdown("<h3>⭐ Rate Your Movies</h3>", unsafe_allow_html=True)
    for movie in df.columns:
        df.loc["You", movie] = st.slider(movie, 0, 5, int(df.loc["You", movie]))

# ---- SIMILARITY & RECOMMENDATION LOGIC ----
similarity = cosine_similarity(df.fillna(0))
sim_df = pd.DataFrame(similarity, index=df.index, columns=df.index)

best_user = sim_df["You"].drop("You").idxmax()

your_ratings = df.loc["You"]

recommended = [
    movie for movie, rating in df.loc[best_user].items()
    if rating >= 4 and your_ratings[movie] == 0
]

unrated = [m for m,v in your_ratings.items() if v == 0]

while len(recommended) < 5 and unrated:
    m = random.choice(unrated)
    if m not in recommended:
        recommended.append(m)

st.subheader("🎬 Movies in System")
st.markdown("<h5 style='text-align:center;color:#888;'>Scroll left to explore</h5>", unsafe_allow_html=True)

scroll_html = "<div style='overflow-x:auto; padding:10px;'><div class='movie-row'>"
for movie,link in poster_links.items():
    scroll_html += f"<div class='movie-box'><img src='{link}' width='140'><div class='caption'>{movie}</div></div>"
scroll_html += "</div></div></div>"

st.markdown(scroll_html, unsafe_allow_html=True)

st.divider()

st.subheader("✅ Top 5 Movie Suggestions For You")
st.markdown(f"👤 **Most similar user → {best_user}**", unsafe_allow_html=True)

st.divider()

cols = st.columns(5)
for i, movie in enumerate(recommended[:5]):
    with cols[i]:
        st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
        st.image(poster_links.get(movie, ""), width=150)
        st.caption(movie)
        st.markdown("</div>", unsafe_allow_html=True)

st.divider()

if st.button("🎲 Pick A Surprise Movie"):
    st.balloons()
    st.write(f"🎉 Your surprise movie → **{random.choice(df.columns)}** 🍿😄")
