import streamlit as st
from google import genai
from google.genai import types
import random

# 1. SYSTEM INITIALIZATION
st.set_page_config(page_title="LUMINA_X_ULTIMATE", page_icon="🧬", layout="wide")

# 2. SECURE API ACCESS
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("SYSTEM_FAILURE: API_KEY_NOT_FOUND.")
    st.stop()

# 3. PERSISTENT STATE & QUOTE ENGINE
if "messages" not in st.session_state:
    st.session_state.messages = []

# Curated Musical Quotes for the "Middle"
MUSICAL_INSIGHTS = [
    "“Music is the arithmetic of sounds as optics is the geometry of light.” — Claude Debussy",
    "“Where words fail, music speaks.” — Hans Christian Andersen",
    "“Do not fear mistakes. There are none.” — Miles Davis",
    "“The air is full of music, you just take as much as you require.” — Edward Elgar",
    "“Music is the shorthand of emotion.” — Leo Tolstoy",
    "“The pause is as important as the note.” — Truman Fisher",
    "“Rhythm and harmony find their way into the inward places of the soul.” — Plato"
]

# 4. THE ULTIMATE AESTHETIC ENGINE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@300;500;700&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at 50% 50%, #1a0633 0%, #020105 100%) !important;
        font-family: 'Rajdhani', sans-serif; 
    }

    /* THE QUOTE CARD - "THE MIDDLE" */
    .insight-card {
        background: linear-gradient(135deg, rgba(188, 19, 254, 0.05), rgba(0, 242, 255, 0.05));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin: 40px auto;
        max-width: 800px;
        text-align: center;
        backdrop-filter: blur(10px);
        animation: glowPulse 4s infinite alternate;
    }

    @keyframes glowPulse {
        from { box-shadow: 0 0 10px rgba(188, 19, 254, 0.1); }
        to { box-shadow: 0 0 30px rgba(0, 242, 255, 0.2); }
    }

    .quote-text {
        font-family: 'Rajdhani';
        font-size: 1.4rem;
        font-style: italic;
        color: #f0f0f0;
        opacity: 0.9;
        line-height: 1.4;
    }

    /* KINETIC NODES */
    @keyframes orbit {
        from { transform: rotate(0deg) translateX(40px) rotate(0deg); }
        to { transform: rotate(360deg) translateX(40px) rotate(-360deg); }
    }
    .orbit-node {
        position: absolute;
        width: 8px; height: 8px;
        background: #00f2ff;
        border-radius: 50%;
        box-shadow: 0 0 15px #00f2ff;
        animation: orbit 4s linear infinite;
        left: 48.5%; top: 15px;
    }

    /* TITLES */
    .studio-title {
        font-family: 'Orbitron';
        font-size: 4.2rem;
        text-align: center;
        background: linear-gradient(90deg, #fff, #bc13fe, #00f2ff, #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% auto;
        animation: shine 10s infinite linear;
        margin-bottom: 0px;
    }
    @keyframes shine { to { background-position: 200% center; } }
</style>
""", unsafe_allow_html=True)

# 5. SIDEBAR: DYNAMIC CONSOLE
with st.sidebar:
    st.markdown('<div style="position:relative; height:100px;"><div class="orbit-node"></div><h1 style="font-family:Orbitron; color:#bc13fe; text-align:center; padding-top:25px;">CORE_OS</h1></div>', unsafe_allow_html=True)
    st.divider()
    expertise = st.selectbox("COMPOSITION_MODE", ["Composer", "Producer", "Sound Designer"])
    fluidity = st.slider("NEURAL_SYNC", 0.0, 1.0, 0.7)
    key_select = st.selectbox("SELECT_KEY", ["C# Minor", "A Major", "G Minor", "D Major", "F# Minor"])

# 6. MAIN VIEWPORT
st.markdown('<p class="studio-title">L U M I N A  S T U D I O</p>', unsafe_allow_html=True)
#st.markdown('<p style="text-align:center; letter-spacing:8px; font-size:0.7rem; color:#00f2ff; opacity:0.6; margin-top:-15px;">BIO_SYNTHETIC // ARCHITECTURE</p>', unsafe_allow_html=True)

# THE MIDDLE: DYNAMIC QUOTE LOGIC
if not st.session_state.messages:
    selected_quote = random.choice(MUSICAL_INSIGHTS)
    st.markdown(f"""
        <div class="insight-card">
            <p style="color:#bc13fe; font-family:Orbitron; font-size:0.7rem; letter-spacing:3px; margin-bottom:15px;">SYSTEM_INSIGHT</p>
            <p class="quote-text">{selected_quote}</p>
        </div>
    """, unsafe_allow_html=True)
else:
    # Display Chat History if messages exist
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 7. INFERENCE ENGINE
if prompt := st.chat_input("TRANSMIT NEURAL FREQUENCY..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        res_placeholder = st.empty()
        full_stream = ""
        with st.status("ENCODING...", expanded=False) as status:
            sys_instruct = f"You are Lumina. Mode: {expertise}. Key: {key_select}. Robotic technical music log only."
            try:
                responses = client.models.generate_content_stream(
                    model="gemini-2.0-flash", 
                    contents=st.session_state.messages[-1]["content"],
                    config=types.GenerateContentConfig(system_instruction=sys_instruct, temperature=fluidity)
                )
                for chunk in responses:
                    full_stream += chunk.text
                    res_placeholder.markdown(full_stream + " ▌")
                status.update(label="ENCODING COMPLETE", state="complete")
            except Exception as e:
                st.error(f"HARDWARE_FAULT: {e}")
        res_placeholder.markdown(full_stream)
        st.session_state.messages.append({"role": "assistant", "content": full_stream})