import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup
import random
import time
import base64
from fpdf import FPDF
import numpy as np
import urllib.parse
# --- 1. CONFIGURATION PRO ---
st.set_page_config(
    page_title="SNIPER OS | REEL DATA", 
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)
def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
        
        :root {
            --primary: #00ff41;
            --background: #0a0a0a;
            --surface: #1a1a1a;
            --text: #e0e0e0;
            --accent: #ff003c;
        }
        .stApp {
            background-color: var(--background);
            color: var(--text);
            font-family: 'Inter', sans-serif;
        }
        .main-header {
            font-family: 'Orbitron', sans-serif;
            color: var(--primary);
            text-align: center;
            padding: 1.5rem 0;
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
            border-bottom: 2px solid var(--primary);
            margin-bottom: 2rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            height: 4em;
            background-color: var(--primary) !important;
            color: black !important;
            font-weight: 900;
            font-family: 'Orbitron', sans-serif;
            border: none;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.4);
            font-size: 1.1rem;
        }
        .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        .stTabs [data-baseweb="tab"] {
            background-color: #111;
            border: 1px solid #333;
            border-radius: 8px 8px 0 0;
            padding: 15px 25px;
            color: #888;
            font-family: 'Orbitron', sans-serif;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--surface) !important;
            color: var(--primary) !important;
            border-color: var(--primary) !important;
        }
        /* Mobile specific adjustments */
        @media (max-width: 600px) {
            .main-header { font-size: 1.5rem; }
            .stMetric { background: #111; padding: 10px; border-radius: 10px; border: 1px solid #333; }
        }
        </style>
    """, unsafe_allow_html=True)
local_css()
# --- 2. FONCTIONS D'EXTRACTION RÉELLE (MÉTHODE SMART) ---
def get_amazon_data(niche):
    """
    Scraper Amazon avec rotation d'User-Agents et gestion de structure réelle.
    """
    query = urllib.parse.quote_plus(niche)
    url = f"https://www.amazon.fr/s?k={query}"
    
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    ]
    
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Device-Memory": "8",
        "Viewport-Width": "1920"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        # Si Amazon nous bloque (Captcha), on utilise un message clair
        if "captcha" in response.text.lower() or response.status_code != 200:
            return None, "🔒 AMAZON BLOCK : Amazon a détecté un robot. Veuillez réessayer dans 1 minute ou utiliser un VPN."
        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.find_all("div", {"data-component-type": "s-search-result"})
        
        if not items:
            return None, "📭 AUCUN PRODUIT : Amazon n'a retourné aucun résultat pour cette recherche."
        results = []
        for i in items:
            try:
                # Titre
                title_tag = i.h2
                title = title_tag.text.strip() if title_tag else "N/A"
                
                # Prix (Extraction complexe pour gérer les virgules et fractions)
                price = 0.0
                price_whole = i.find("span", "a-price-whole")
                price_fraction = i.find("span", "a-price-fraction")
                if price_whole:
                    p_str = price_whole.text.replace(',', '').replace('\xa0', '').strip()
                    p_frac = price_fraction.text.strip() if price_fraction else "00"
                    price = float(f"{p_str}.{p_frac}")
                
                # Note
                rating = 0.0
                rating_tag = i.find("span", {"class": "a-icon-alt"})
                if rating_tag:
                    rating = float(rating_tag.text.split()[0].replace(',', '.'))
                
                # Avis
                reviews = 0
                reviews_tag = i.find("span", {"class": "a-size-base", "dir": "auto"})
                if reviews_tag and "vendu" not in reviews_tag.text.lower():
                    rev_text = reviews_tag.text.replace('\xa0', '').replace(' ', '').replace(',', '').strip()
                    if rev_text.isdigit():
                        reviews = int(rev_text)
                if price > 0: # On n'ajoute que les produits avec un prix détecté
                    results.append({
                        "Produit": title[:70] + "...",
                        "Prix (€)": price,
                        "Note (⭐️)": rating,
                        "Avis": reviews,
                        "Lien": "https://www.amazon.fr" + i.find("a", {"class": "a-link-normal s-no-outline"})['href'] if i.find("a") else "#"
                    })
            except Exception:
                continue
                
        if not results:
            return None, "⚠️ ERREUR STRUCTURE : Impossible de lire les prix sur cette page Amazon."
            
        return pd.DataFrame(results), None
    except Exception as e:
        return None, f"🌋 ERREUR CRITIQUE : {str(e)}"
# --- 3. DASHBOARD ---
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'real_data' not in st.session_state:
    st.session_state.real_data = None
st.markdown("<h1 class='main-header'>🎯 SNIPER OS : LIVE AMAZON</h1>", unsafe_allow_html=True)
# Barre de recherche optimisée mobile
col_search, col_btn = st.columns([3, 1])
with col_search:
    niche = st.text_input("", placeholder="Entrez votre niche (ex: Aspirateur Robot)", label_visibility="collapsed")
with col_btn:
    search_trigger = st.button("🚀 SCAN")
if search_trigger and niche:
    with st.spinner("🛰️ INFILTRATION DES SERVEURS AMAZON FR..."):
        df, error = get_amazon_data(niche)
        if error:
            st.error(error)
            st.info("💡 CONSEIL : Si vous êtes sur Streamlit Cloud, Amazon bloque souvent les IPs. Essayez de relancer ou d'utiliser une niche différente.")
        else:
            st.session_state.real_data = df
            st.session_state.search_query = niche
            st.success(f"✅ {len(df)} Concurrents Réels Détectés !")
# Affichage des résultats
if st.session_state.real_data is not None:
    df = st.session_state.real_data
    
    t1, t2, t3 = st.tabs(["📊 MARCHÉ RÉEL", "💰 CALCULATEUR", "📝 SCRIPT"])
    
    with t1:
        st.subheader(f"Analyse Directe : {st.session_state.search_query.upper()}")
        
        m1, m2, m3 = st.columns(3)
        avg_p = df["Prix (€)"].mean()
        m1.metric("PRIX MOYEN", f"{round(avg_p, 2)} €")
        m2.metric("AVIS MAX", f"{df['Avis'].max()}")
        m3.metric("NOTE MOYENNE", f"{round(df['Note (⭐️)'].mean(), 1)}/5")
        
        # Table de données avec liens cliquables
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.download_button("📥 Télécharger DATA (CSV)", df.to_csv(index=False), "data_amazon.csv")
    with t2:
        st.subheader("Simulateur de Profit Net")
        c1, c2 = st.columns(2)
        with c1:
            sell_p = st.number_input("Prix de Vente (€)", value=float(round(avg_p, 2)))
            buy_p = st.number_input("Coût Achat DDP (€)", value=10.0)
        
        with c2:
            # Calcul rapide (Frais Amazon ~15% + FBA ~5€)
            fees = (sell_p * 0.15) + 5.0
            profit = sell_p - buy_p - fees
            roi = (profit / buy_p) * 100 if buy_p > 0 else 0
            
            st.metric("NET PROFIT", f"{round(profit, 2)} €", delta=f"{round(roi, 1)}% ROI")
            if profit > 10: st.success("🎯 NICHE VALIDÉE")
            else: st.warning("⚠️ MARGE FAIBLE")
    with t3:
        st.subheader("Script UGC Automatique")
        st.code(f"""
[HOOK] : "J'ai trouvé le meilleur {st.session_state.search_query} sur Amazon..."
[POINT FORT] : "Il coûte seulement {round(avg_p, 2)}€ en moyenne alors que la qualité est folle."
[ACTION] : "Lien en bio pour profiter de la promo !"
        """, language="markdown")
else:
    st.info("Entrez une niche ci-dessus pour extraire les données réelles d'Amazon.")
st.markdown("---")
st.caption("Données en direct de Amazon.fr - Sniper OS Pro v5.1")
