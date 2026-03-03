import streamlit as st
import pandas as pd
import numpy as np

# 1. SETUP ELITE
st.set_page_config(page_title="DATA SNIPER OS", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #020202; color: #e0e0e0; }
    .stMetric { background-color: #0a0a0a; border: 1px solid #00ff00; padding: 20px; border-radius: 10px; }
    h1 { color: #00ff00; text-shadow: 0 0 20px #00ff00; text-align: center; font-size: 3.5rem !important; }
    .data-card { background: #111; border-radius: 15px; padding: 25px; border-left: 8px solid #00ff00; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("# 💎 DATA SNIPER : REEL")

# 2. MENU
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/11516/11516751.png", width=80)
    menu = st.radio("INTELLIGENCE", ["📊 ANALYSE DE NICHE REELLE", "💰 CALCULATEUR DE MARGE FBA", "📦 SOURCING DATA"])
    st.divider()
    st.write("UTILISATEUR: ELITE")
    st.info("CODE: VIBECUT")

# 3. ANALYSE DE NICHE REELLE
if menu == "📊 ANALYSE DE NICHE REELLE":
    st.subheader("🔍 Analyseur de Marche en Temps Reel")
    niche = st.text_input("Produit a scanner (ex: Correcteur de posture)", "")
   
    if niche:
        col1, col2, col3 = st.columns(3)
       
        # Données réelles via liens profonds
        with col1:
            st.markdown("<div class='data-card'>", unsafe_allow_html=True)
            st.write("### 🌍 Demande Mondiale")
            st.link_button("VOIR TENDANCE REELLE (Google)", f"https://trends.google.com/trends/explore?q={niche}")
            st.caption("Verifie si la demande monte ou descend sur 12 mois.")
            st.markdown("</div>", unsafe_allow_html=True)
           
        with col2:
            st.markdown("<div class='data-card'>", unsafe_allow_html=True)
            st.write("### 📦 Analyse Concurrence")
            st.link_button("SCANNER LES AVIS (Amazon)", f"https://www.amazon.fr/s?k={niche}&i=specialty-aps&s=review-rank")
            st.caption("Cherche les produits avec 3 etoiles : c'est LA que sont les failles.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<div class='data-card'>", unsafe_allow_html=True)
            st.write("### 🎥 Analyse Sociale")
            st.link_button("VOLUME TIKTOK / ADS", f"https://www.tiktok.com/search?q={niche}")
            st.caption("Mesure la viralite du produit.")
            st.markdown("</div>", unsafe_allow_html=True)

# 4. CALCULATEUR FBA (PRECIS)
elif menu == "💰 CALCULATEUR DE MARGE FBA":
    st.subheader("💵 Calcul de Profit Reel (Algorithme Amazon)")
   
    col_a, col_b = st.columns(2)
    with col_a:
        prix_vente = st.number_input("Prix de vente public (€)", value=29.90)
        poids = st.number_input("Poids du colis (kg)", value=0.5)
       
    with col_b:
        cout_total_achat = st.number_input("Cout d'achat unitaire (Produit + Transport Chine/FBA) (€)", value=8.50)
        ads = st.slider("Budget Pub (PPC) par vente (€)", 1.0, 15.0, 5.0)

    # Calcul des vrais frais FBA (Estimation basee sur grille Amazon 2024)
    comm_amazon = prix_vente * 0.15
    frais_envoi_fba = 4.50 if poids < 1 else 7.50
    total_frais = comm_amazon + frais_envoi_fba + ads
    profit_net = prix_vente - cout_total_achat - total_frais
    marge_pourcent = (profit_net / prix_vente) * 100

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("PROFIT NET / UNITE", f"{round(profit_net, 2)} €")
    m2.metric("MARGE NETTE (%)", f"{int(marge_pourcent)} %")
    m3.metric("FRAIS AMAZON TOTAL", f"{round(total_frais, 2)} €")
   
    if marge_pourcent < 20:
        st.error("⚠️ MARGE FAIBLE : Risque eleve. Cherchez un meilleur prix d'achat.")
    else:
        st.success("✅ MARGE ELITE : Produit valide pour le lancement.")

# 5. SOURCING DATA
elif menu == "📦 SOURCING DATA":
    st.subheader("🚢 Base de Sourcing Monde")
    product_find = st.text_input("Produit a sourcer :")
    if product_find:
        st.write("### Comparaison Fournisseurs Reelle")
        st.link_button("RECHERCHE ALIBABA (Prix Gros)", f"https://www.alibaba.com/trade/search?SearchText={product_find}")
        st.link_button("RECHERCHE 1688 (Prix Chine Direct)", f"https://s.1688.com/selloffer/offer_search.htm?keywords={product_find}")
        st.info("Astuce : 1688 est souvent 30% moins cher qu'Alibaba.")

 
