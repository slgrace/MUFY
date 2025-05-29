import streamlit as st
import requests
import time

# ===== THEME SYSTEM =====
THEMES = {
    "🤡 Circus": {
        "primary": "#FF6B6B",
        "background": "#FFF5E6",
        "secondary": "#FF9E7D"
    },
    "🧙‍♂️ Wizard": {
        "primary": "#6B5B95",
        "background": "#F0E6FF",
        "secondary": "#9E7DFF"
    },
    "🐉 Dragon": {
        "primary": "#CC0000",
        "background": "#FFE6E6",
        "secondary": "#FF6B6B"
    }
}

# ===== SETUP PAGE =====
st.set_page_config(page_title="Laugh Box", page_icon="😂")

# ===== SIDEBAR THEME SELECTOR =====
current_theme = st.sidebar.selectbox(
    "Choose Theme", 
    list(THEMES.keys()),
    key="theme_selector"
)

# Apply selected theme
theme = THEMES[current_theme]
st.markdown(f"""
<style>
    .stApp {{
        background-color: {theme['background']};
    }}
    h1, h2, h3 {{
        color: {theme['primary']} !important;
    }}
    .stButton>button {{
        background-color: {theme['secondary']} !important;
        color: white !important;
    }}
    .joke-box {{
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: white;
        margin: 1rem 0;
        border-left: 5px solid {theme['primary']};
    }}
</style>
""", unsafe_allow_html=True)

# ===== MAIN APP =====
st.title(f"{current_theme.split()[0]} Laugh Box")
st.write(f"Current theme: **{current_theme}**")

# Joke categories
CATEGORIES = {
    "Random": "any",
    "Programming": "programming",
    "Pun": "pun"
}

# User inputs
category = st.selectbox("Joke Category", list(CATEGORIES.keys()))
delivery_style = st.radio(
    "Delivery Style", 
    ["Normal", "Dramatic"], 
    horizontal=True
)

# Joke fetching function
def get_joke():
    url = f"https://v2.jokeapi.dev/joke/{CATEGORIES[category]}"
    try:
        response = requests.get(url, timeout=3)
        data = response.json()
        if data.get("error", False):
            return "Why did the joke fail?", "Because the API needed a break!"
        if data["type"] == "twopart":
            return data["setup"], data["delivery"]
        return data["joke"], None
    except:
        return "Why couldn't we load a joke?", "Because the internet is telling its own jokes!"

# Joke display
if st.button("Tell Me a Joke!"):
    with st.spinner("Preparing your joke..."):
        if delivery_style == "Dramatic":
            time.sleep(2)
        
        setup, punchline = get_joke()
        
        with st.container():
            st.markdown('<div class="joke-box">', unsafe_allow_html=True)
            st.write(f"**{setup}**")
            if punchline:
                if delivery_style == "Dramatic":
                    time.sleep(1)
                st.write(f"*{punchline}*")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Theme-specific celebration
        if "Circus" in current_theme:
            st.balloons()
        elif "Dragon" in current_theme:
            st.snow()

# Footer
st.markdown("---")
st.caption("Switch themes in the sidebar for a different experience!")