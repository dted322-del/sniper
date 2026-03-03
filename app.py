import streamlit as st

# 1. STYLE LUXE (Toujours sans accents pour eviter les bugs)
st.set_page_config(page_title="SNIPER OS", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    h1 { color: #00ff00; text-shadow: 0 0 10px #00ff00; text-align: center; font-family: sans-serif; }
    .stButton>button { background-color: #00ff00; color: black; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_stdio=True)

st.markdown("# 💎 SNIPER OS : ELITE EDITION")

# 2. NAVIGATION
menu = st.sidebar.radio("COMMANDES", ["🚀 RADAR", "📈 PROFITS", "🛡️ VALIDATEUR"])

if menu == "🚀 RADAR":
    st.subheader("Analyseur de Failles Amazon")
    niche = st.text_input("Quelle niche analyser ?", "Yoga")
    st.link_button(f"VOIR LES FAILLES : {niche.upper()}", f"https://www.amazon.fr/s?k={niche}")

if menu == "📈 PROFITS":
    st.subheader("Calculateur de Liberté")
    ca = st.number_input("CA Mensuel vise (€)", value=5000)
    marge = st.slider("Marge Nette (%)", 10, 50, 25)
    profit = int(ca * (marge/100))
    st.metric("PROFIT NET MENSUEL", f"{profit} €")
    st.info(f"Soit {profit * 12} € par an.")

if menu == "🛡️ VALIDATEUR":
    st.subheader("Criteres Anti-Echec")
    c1 = st.checkbox("Poids < 1.2kg")
    c2 = st.checkbox("Prix > 35€")
    c3 = st.checkbox("Avis concurrents < 4.2 stars")
    if c1 and c2 and c3:
        st.success("FEU VERT : PRODUIT GAGNANT")
    else:
        st.warning("ATTENTION : Verifiez les criteres manquants")

st.sidebar.write("---")
st.sidebar.info("Code UGC : VIBECUT")

 
