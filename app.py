st.markdown("""
    <style>
    /* 1. THEME OVERRIDE */
    :root {
        --primary-color: #00d1b2;
        --background-color: #ffffff;
        --secondary-background-color: #f0f2f6;
        --text-color: #000000;
        --font: "Source Sans Pro", sans-serif;
    }

    /* 2. BACKGROUND */
    .stApp {
        background: linear-gradient(rgba(255,255,255,0.8), rgba(255,255,255,0.8)), 
                    url("https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
    }

    /* 3. INPUT BOXES - TOTAL FORCE WHITE */
    div[data-baseweb="input"], div[data-baseweb="select"], .stNumberInput input {
        background-color: white !important;
        background: white !important;
        color: black !important;
        -webkit-text-fill-color: black !important;
        border: 3px solid #00d1b2 !important;
    }

    /* 4. TEXT COLORS - TOTAL FORCE BLACK */
    h1, h2, h3, p, label, .stMarkdown, .stMetric div {
        color: black !important;
        fill: black !important;
    }
    
    /* 5. TABLE FIX */
    .stTable td { color: black !important; background-color: white !important; }
    </style>
    """, unsafe_allow_html=True)
