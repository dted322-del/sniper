import streamlit as st

# 1. CONFIGURATION & STYLE
st.set_page_config(page_title="SNIPER OS", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    h1 { color: #00ff00; text-shadow: 0 0 10px #00ff00; text-align: center; }
    .stMetric { background-color: #111; border: 1px solid #222; padding: 15px; border-radius: 10px; border-left: 5px solid #00ff00; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("# 💎 SNIPER OS : ELITE EDITION")

# 2. NAVIGATION SIDEBAR
with st.sidebar:
    st.title("MENU")
    menu = st.radio("Navigation", ["🚀 RADAR", "📈 PROFITS", "🛡️ VALIDATEUR"])
    st.write("---")
    st.info("Code : VIBECUT")

# 3. CONTENU DES ONGLETS
if menu == "🚀 RADAR":
    st.subheader("Analyseur de Failles Amazon")
    niche = st.text_input("Quelle niche analyser ?", "Yoga")
    st.link_button(f"RECHERCHER : {niche.upper()}", f"https://www.amazon.fr/s?k={niche}")

elif menu == "📈 PROFITS":
    st.subheader("Calculateur de Rentabilite")
    c1, c2 = st.columns(2)
    with c1:
        ca = st.number_input("Objectif CA Mensuel (€)", value=5000)
    with c2:
        marge = st.slider("Marge Nette (%)", 10, 50, 25)
   
    profit = int(ca * (marge/100))
    st.metric("PROFIT NET ESTIMÉ", f"{profit} €")

elif menu == "🛡️ VALIDATEUR":
    st.subheader("Criteres Anti-Echec")
    c1 = st.checkbox("Poids < 1.2kg")
    c2 = st.checkbox("Prix > 35€")
    c3 = st.checkbox("Avis concurrents < 4.2 stars")
    if c1 and c2 and c3:
        st.success("FEU VERT : PRODUIT HAUT POTENTIEL")
    else:
        st.warning("ANALYSE : Verifiez les criteres")

 
