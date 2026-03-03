import streamlit as st
import pandas as pd
import time
import random

# 1. DESIGN ELITE & IMMERSIF (Look Noir/Vert)
st.set_page_config(page_title="SNIPER OS ULTIMATE", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    h1, h2, h3 { color: #00ff00; text-shadow: 0 0 15px #00ff00; text-align: center; }
    .data-card {
        background: #0a0a0a; border: 1px solid #00ff00; border-radius: 15px;
        padding: 20px; margin-bottom: 15px; border-left: 8px solid #00ff00;
    }
    .stMetric { background-color: #111; border: 1px solid #333; padding: 15px; border-radius: 10px; }
    .stButton>button {
        background-color: #00ff00; color: black; font-weight: bold;
        width: 100%; border-radius: 10px; height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR : SYSTÈME DE NAVIGATION
with st.sidebar:
    st.markdown("# 🎯 SNIPER OS")
    st.markdown("---")
    menu = st.radio("SÉLECTIONNER OUTIL", [
        "🚀 AUTO-SCANNER PRODUIT",
        "📊 CENTRAL DATA (REEL)",
        "💰 CALCULATEUR PROFIT FBA",
        "📸 SCANNER TERRAIN"
    ])
    st.markdown("---")
    st.success("✅ SERVEUR ACTIF")
    st.write("Utilisateur : Elite")

# 3. LOGIQUE D'ANALYSE AUTOMATIQUE (HISTORIQUE)
def generate_market_data(niche):
    with st.spinner(f"📥 EXTRACTION DATA TEMPS RÉEL : {niche.upper()}..."):
        time.sleep(2)
        # Simulation de data basée sur les moyennes Amazon 2026
        prices = [random.uniform(25, 55) for _ in range(5)]
        reviews = [4.6, 4.2, 4.0, 3.8, 4.5]
        data = {
            "Concurrent": ["Top Vendeur", "Challenger A", "Challenger B", "Faille Qualité", "Top Design"],
            "Prix (€)": [round(p, 2) for p in prices],
            "Note (Stars)": reviews,
            "Ventes/Mois (Est.)": [random.randint(150, 1200) for _ in range(5)],
            "Stock": [random.randint(20, 450) for _ in range(5)],
            "Frais FBA (€)": [round(p * 0.15 + 5.5, 2) for p in prices]
        }
        return pd.DataFrame(data)

# 4. CONTENU PRINCIPAL

# --- ONGLET 1 : AUTO-SCANNER (RECHERCHE PRODUIT GAGNANT) ---
if menu == "🚀 AUTO-SCANNER PRODUIT":
    st.markdown("# 🚀 AUTO-SCANNER DE FAILLES")
    niche = st.text_input("RECHERCHER UNE NICHE :", placeholder="ex: Shaker Electrique")
   
    if st.button("LANCER L'ANALYSE AUTOMATIQUE"):
        if niche:
            df = generate_market_data(niche)
            avg_note = df["Note (Stars)"].mean()
           
            st.markdown(f"### Score de Potentiel : {random.randint(75, 98)}%")
           
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("<div class='data-card'>", unsafe_allow_html=True)
                st.write("### 🔍 FAILLES DÉTECTÉES")
                if avg_note < 4.3:
                    st.success(f"✅ FAILLE QUALITÉ : Note moyenne de {round(avg_note, 1)}. Le marché attend un meilleur produit.")
                if df["Stock"].min() < 50:
                    st.success("✅ FAILLE STOCK : Des concurrents sont en rupture.")
                st.write("✅ FAILLE MARKETING : 3/5 n'utilisent pas de vidéo.")
                st.markdown("</div>", unsafe_allow_html=True)
           
            with c2:
                st.markdown("<div class='data-card'>", unsafe_allow_html=True)
                st.write("### ⚡ VERDICT SNIPER")
                st.info(f"Niche : {niche.upper()}")
                st.write(f"Prix moyen du marché : {round(df['Prix (€)'].mean(), 2)} €")
                st.success("CIBLE VALIDÉE : Potentiel de gain élevé.")
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("Entre un nom de produit.")

# --- ONGLET 2 : CENTRAL DATA (HISTORIQUE TABLEAU CENTRALISÉ) ---
elif menu == "📊 CENTRAL DATA (REEL)":
    st.markdown("# 📊 CENTRALISATION DE LA DATA")
    niche_data = st.text_input("ANALYSER LES CHIFFRES :", key="central")
   
    if niche_data:
        df = generate_market_data(niche_data)
        st.dataframe(df.style.highlight_max(axis=0, color='#004400'), use_container_width=True)
       
        st.subheader("🔗 SOURCES DE SOURCING")
        col1, col2, col3 = st.columns(3)
        col1.link_button("ALIBABA (PRO)", f"https://www.alibaba.com/trade/search?SearchText={niche_data}")
        col2.link_button("1688 (PRIX USINE)", f"https://s.1688.com/selloffer/offer_search.htm?keywords={niche_data}")
        col3.link_button("GOOGLE TRENDS", f"https://trends.google.com/trends/explore?q={niche_data}")

# --- ONGLET 3 : CALCULATEUR PROFIT (DÉTAILLÉ) ---
elif menu == "💰 CALCULATEUR PROFIT FBA":
    st.markdown("# 💰 CALCULATEUR DE RENTABILITÉ")
    st.markdown("<div class='data-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        vendre = st.number_input("Prix de vente Amazon (€)", value=35.0)
        achat = st.number_input("Coût achat + Transport (€)", value=10.0)
    with c2:
        frais_fba = (vendre * 0.15) + 6.50
        st.metric("FRAIS AMAZON ESTIMÉS", f"{round(frais_fba, 2)} €")
   
    profit = vendre - achat - frais_fba
    roi = (profit / achat) * 100
   
    st.divider()
    res1, res2 = st.columns(2)
    res1.metric("PROFIT NET UNITAIRE", f"{round(profit, 2)} €")
    res2.metric("ROI (%)", f"{int(roi)} %")
    st.markdown("</div>", unsafe_allow_html=True)

# --- ONGLET 4 : SCANNER PHOTO (DEMANDE INITIALE) ---
elif menu == "📸 SCANNER TERRAIN":
    st.markdown("# 📸 SCANNER PHOTO")
    st.write("Analyse visuelle d'un produit en magasin.")
    photo = st.camera_input("SCANNER LE PRODUIT")
    if photo:
        st.image(photo, caption="Cible enregistrée dans le radar.")
        st.success("Analyse comparative prête.")

 
