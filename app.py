import pickle
import pandas as pd
import streamlit as st
import requests

st.set_page_config(
    page_title="Movie Recommender",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Design Tokens ── */
:root {
    --bg:           #0B0B0B;
    --surface:      #1e1e1e;
    --surface2:     #252525;
    --red:          #E50914;
    --red-dark:     #b20710;
    --red-glow:     rgba(229,9,20,0.30);
    --text:         #FFFFFF;
    --muted:        #a3a3a3;
    --border:       rgba(255,255,255,0.10);
    --glass-bg:     rgba(30,30,30,0.85);
    --glass-border: rgba(255,255,255,0.12);
    --card-shadow:  0 8px 32px rgba(0,0,0,0.65);
    --ease:         cubic-bezier(0.25,0.46,0.45,0.94);
}

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box; }

/* ── App background & font ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    overflow-x: hidden;
}

/* ── Hide all Streamlit chrome ── */
#MainMenu,
footer,
header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stSidebar"],
.viewerBadge_container__1QSob { display: none !important; }

/* ── Remove default page padding ── */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--red); border-radius: 3px; }


.hero {
    position: relative;
    width: 100%;
    min-height: 320px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 64px 24px 48px;
    overflow: hidden;
    background:
        radial-gradient(ellipse 80% 55% at 50% 0%,
            rgba(229,9,20,0.16) 0%, transparent 70%),
        var(--bg);
}

.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        repeating-linear-gradient(90deg,
            transparent 0px, transparent 119px,
            rgba(229,9,20,0.04) 119px, rgba(229,9,20,0.04) 120px),
        repeating-linear-gradient(0deg,
            transparent 0px, transparent 79px,
            rgba(255,255,255,0.012) 79px, rgba(255,255,255,0.012) 80px);
    pointer-events: none;
}

.hero::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--red), transparent);
}

.hero-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--red);
    margin-bottom: 16px;
    animation: fadeUp 0.6s var(--ease) both 0.1s;
}

.hero-title {
    font-size: clamp(2.4rem, 6vw, 5rem);
    font-weight: 900;
    line-height: 1.08;
    letter-spacing: -0.03em;
    margin-bottom: 20px;
    background: linear-gradient(135deg,
        #fff 0%, #fff 30%, var(--red) 52%, #ff6b6b 68%, #fff 88%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation:
        fadeUp 0.7s var(--ease) both 0.25s,
        shimmer 5s linear infinite 1.2s;
}

.hero-sub {
    font-size: clamp(0.9rem, 2vw, 1.1rem);
    font-weight: 400;
    color: var(--muted);
    max-width: 500px;
    line-height: 1.7;
    animation: fadeUp 0.7s var(--ease) both 0.4s;
}

.hero-divider {
    width: 56px;
    height: 3px;
    background: var(--red);
    border-radius: 2px;
    margin: 24px auto 0;
    animation: fadeUp 0.7s var(--ease) both 0.52s;
}




.search-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 14px;
    display: block;
}

/* ── Hide ALL native Streamlit selectbox labels ── */
[data-testid="stSelectbox"] label,
div[data-testid="stSelectbox"] > label,
.stSelectbox label {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* ── Selectbox trigger ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    min-height: 52px !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 3px var(--red-glow) !important;
}

/* Selected value text */
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] div[class*="singleValue"],
[data-testid="stSelectbox"] div[class*="placeholder"],
[data-testid="stSelectbox"] input {
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
}


[data-testid="stSelectbox"] svg { color: var(--red) !important; fill: var(--red) !important; }

/* ── Dropdown popover / listbox ── */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="popover"] > div > div {
    background: #222222 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

[data-baseweb="menu"],
ul[role="listbox"] {
    background: #222222 !important;
    padding: 4px !important;
}

li[role="option"],
[data-baseweb="menu"] li,
[role="option"],
[data-baseweb="option"] {
    background: #222222 !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 400 !important;
    border-radius: 6px !important;
    padding: 10px 14px !important;
    cursor: pointer !important;
    transition: background 0.15s ease !important;
}
li[role="option"]:hover,
[data-baseweb="menu"] li:hover,
[data-baseweb="option"]:hover {
    background: rgba(229,9,20,0.20) !important;
    color: #ffffff !important;
}
li[aria-selected="true"],
[aria-selected="true"],
[data-baseweb="option"][aria-selected="true"] {
    background: rgba(229,9,20,0.25) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}


[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--red) 0%, var(--red-dark) 100%) !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 15px 32px !important;
    margin-top: 14px !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
    transition: transform 0.25s var(--ease), box-shadow 0.25s var(--ease) !important;
    box-shadow: 0 4px 20px rgba(229,9,20,0.38) !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(229,9,20,0.55) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}


.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}
.section-bar {
    width: 4px; height: 24px;
    background: var(--red);
    border-radius: 2px;
    flex-shrink: 0;
}
.section-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.01em;
}
.section-badge {
    margin-left: auto;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--red);
    background: rgba(229,9,20,0.10);
    border: 1px solid rgba(229,9,20,0.22);
    border-radius: 20px;
    padding: 3px 10px;
}


.featured-wrap {
    max-width: 820px;
    margin: 0 auto 48px;
    padding: 0 24px;
}

.featured-card {
    display: flex;
    align-items: flex-start;
    gap: 28px;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow: var(--card-shadow);
    animation: fadeUp 0.5s var(--ease) both;
}
.featured-poster-img {
    width: 120px;
    min-width: 120px;
    aspect-ratio: 2/3;
    object-fit: cover;
    border-radius: 10px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.6);
    display: block;
}
.featured-poster-fallback {
    width: 120px;
    min-width: 120px;
    aspect-ratio: 2/3;
    background: #2a2a2a;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
}
.featured-info { flex: 1; min-width: 0; }
.feat-label {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--red);
    margin-bottom: 8px;
}
.feat-title {
    font-size: clamp(1.2rem, 3vw, 1.8rem);
    font-weight: 800;
    line-height: 1.2;
    letter-spacing: -0.02em;
    color: var(--text);
    margin-bottom: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.feat-meta {
    font-size: 0.76rem;
    color: #888;
    font-weight: 600;
    margin-bottom: 10px;
}
.feat-overview {
    font-size: 0.86rem;
    color: var(--muted);
    line-height: 1.65;
}

.recs-outer {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 24px 80px;
}

.cards-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 18px;
}
@media (max-width: 1100px) { .cards-grid { grid-template-columns: repeat(4, 1fr); } }
@media (max-width: 860px)  { .cards-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 560px)  { .cards-grid { grid-template-columns: repeat(2, 1fr); } }

.movie-card {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    background: var(--surface);
    border: 1px solid var(--border);
    cursor: pointer;
    will-change: transform;
    box-shadow: var(--card-shadow);
    transition: transform 0.32s var(--ease),
                border-color 0.32s ease,
                box-shadow 0.32s ease;
    animation: fadeUp 0.5s var(--ease) both;
}

.movie-card:hover {
    transform: translateY(-10px) scale(1.035);
    border-color: rgba(229,9,20,0.45);
    box-shadow:
        0 22px 55px rgba(0,0,0,0.75),
        0 0 28px rgba(229,9,20,0.22);
}

.card-poster {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
    transition: transform 0.32s var(--ease);
}
.movie-card:hover .card-poster { transform: scale(1.04); }

.card-fallback {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #222 0%, #2d2d2d 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-size: 2.2rem;
}
.card-fallback span {
    font-size: 0.7rem;
    color: var(--muted);
    font-weight: 500;
}

.card-overlay {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(0deg,
        rgba(0,0,0,0.95) 0%,
        rgba(0,0,0,0.45) 55%,
        transparent 100%);
    padding: 36px 12px 13px;
}

.card-rank {
    font-size: 0.63rem;
    font-weight: 700;
    color: var(--red);
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.card-title {
    font-size: 0.8rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}


.site-footer {
    border-top: 1px solid var(--border);
    padding: 36px 24px;
    text-align: center;
}
.footer-chips {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
    margin-bottom: 18px;
}
.chip {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: var(--muted);
    background: rgba(255,255,255,0.06);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 4px 13px;
}
.footer-copy {
    font-size: 0.74rem;
    color: rgba(255,255,255,0.22);
}
.footer-copy em { color: var(--red); font-style: normal; }


@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes shimmer {
    0%   { background-position: 0% center; }
    50%  { background-position: 100% center; }
    100% { background-position: 0% center; }
}


[data-testid="column"] { padding: 0 !important; }
div[class*="stMarkdown"] p { margin: 0; }


.element-container { margin: 0 !important; }
</style>
""", unsafe_allow_html=True)



@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies      = pd.DataFrame(movies_dict)
    similarity  = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()
movie_list = movies['title'].values



TMDB_KEY = "8265bd1679663a7ea12ac168da84d2e8"
IMG_BASE  = "https://image.tmdb.org/t/p/w500"

def _tmdb_get(movie_id: int) -> dict:
    try:
        url  = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_KEY}&language=en-US"
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return {}

def fetch_poster(movie_id: int) -> str | None:
    data = _tmdb_get(movie_id)
    path = data.get("poster_path")
    return f"{IMG_BASE}{path}" if path else None

def fetch_movie_details(movie_id: int) -> dict:
    data = _tmdb_get(movie_id)
    path = data.get("poster_path")
    return {
        "poster":   f"{IMG_BASE}{path}" if path else None,
        "overview": data.get("overview") or "",
        "year":     (data.get("release_date") or "")[:4],
        "rating":   data.get("vote_average"),
    }


def recommend(movie: str):
    idx       = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[idx]), key=lambda x: x[1], reverse=True)
    names, posters, ids = [], [], []
    for i, _ in distances[1:6]:
        mid = movies.iloc[i].movie_id
        names.append(movies.iloc[i].title)
        posters.append(fetch_poster(mid))
        ids.append(mid)
    return names, posters, ids



st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-Powered Discovery</div>
    <h1 class="hero-title">Movie Recommender System</h1>
    <p class="hero-sub">
        Tell us what you love — we'll find what to watch next.<br>
        Powered by machine learning &amp; 5,000+ titles.
    </p>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)



_, col_center, _ = st.columns([1, 2.2, 1])

with col_center:

    st.markdown(
        '<span class="search-label">Choose a movie</span>',
        unsafe_allow_html=True
    )

    selected_movie = st.selectbox(
        label="Movie",
        options=movie_list,
        label_visibility="collapsed",
    )

    recommend_clicked = st.button(
        "🎬 Discover Similar Movies",
        use_container_width=True
    )



if selected_movie:
    sel_id  = int(movies[movies['title'] == selected_movie].iloc[0].movie_id)
    details = fetch_movie_details(sel_id)

    overview = details["overview"] or "No overview available."
    if len(overview) > 200:
        overview = overview[:200].rstrip() + "…"

    rating = details["rating"]
    meta_parts = []
    if details["year"]:
        meta_parts.append(details["year"])
    if rating and float(rating) > 0:
        meta_parts.append(f"⭐ {float(rating):.1f}")
    meta_str = "  ·  ".join(meta_parts)

    if details["poster"]:
        poster_html = f'<img class="featured-poster-img" src="{details["poster"]}" alt="{selected_movie}" />'
    else:
        poster_html = '<div class="featured-poster-fallback">🎬</div>'

    st.markdown("<br>", unsafe_allow_html=True)
    _, fc, _ = st.columns([1, 2.2, 1])
    with fc:
        st.markdown(f"""
<div class="featured-wrap">
    <div class="section-header">
        <div class="section-bar"></div>
        <div class="section-title">Currently Selected</div>
    </div>
    <div class="featured-card">
        {poster_html}
        <div class="featured-info">
            <div class="feat-label">Your Pick</div>
            <div class="feat-title">{selected_movie}</div>
            <div class="feat-meta">{meta_str}</div>
            <div class="feat-overview">{overview}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)



if recommend_clicked:
    st.markdown("<br>", unsafe_allow_html=True)

    with st.spinner("Finding your next watch…"):
        names, posters, rec_ids = recommend(selected_movie)


    st.markdown("""
<div class="recs-outer">
    <div class="section-header">
        <div class="section-bar"></div>
        <div class="section-title">Because You Liked That…</div>
        <div class="section-badge">Top 5 Picks</div>
    </div>
</div>
""", unsafe_allow_html=True)

    cols = st.columns(5, gap="medium")

    for idx, (name, poster, _) in enumerate(zip(names, posters, rec_ids)):
        rank = f"#{idx + 1} Pick"
        with cols[idx]:
            if poster:
                media_html = f'<img class="card-poster" src="{poster}" alt="{name}" style="width:100%;border-radius:10px 10px 0 0;display:block;" />'
            else:
                media_html = '<div class="card-fallback" style="width:100%;aspect-ratio:2/3;background:linear-gradient(135deg,#222,#2d2d2d);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;font-size:2rem;border-radius:10px 10px 0 0;">🎬<span style="font-size:0.7rem;color:#a3a3a3;font-weight:500;">No Poster</span></div>'

            st.markdown(f"""
<div class="movie-card" style="border-radius:12px;overflow:hidden;background:#1e1e1e;border:1px solid rgba(255,255,255,0.10);cursor:pointer;box-shadow:0 8px 32px rgba(0,0,0,0.65);transition:transform 0.32s ease,border-color 0.32s ease,box-shadow 0.32s ease;margin-bottom:8px;">
    {media_html}
    <div style="padding:12px;">
        <div style="font-size:0.63rem;font-weight:700;color:#E50914;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:4px;">{rank}</div>
        <div style="font-size:0.82rem;font-weight:700;color:#fff;line-height:1.3;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;">{name}</div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)



st.markdown("""
<div class="site-footer">
    <div class="footer-chips">
        <span class="chip">Python</span>
        <span class="chip">Streamlit</span>
        <span class="chip">Pandas</span>
        <span class="chip">Scikit-Learn</span>
        <span class="chip">Cosine Similarity</span>
        <span class="chip">TMDB API</span>
        <span class="chip">Pickle</span>
    </div>
</div>
""", unsafe_allow_html=True)