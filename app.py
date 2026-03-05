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
from collections import Counter
import re
# --- 1. CONFIGURATION ÉLITE ---
st.set_page_config(
    page_title="SNIPER OS | REEL FR DATA", 
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)
def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
        :root { --primary: #00ff41; --background: #020202; --surface: #0a0a0a; --text: #ffffff; }
        .stApp { background-color: var(--background); color: var(--text); font-family: 'Inter', sans-serif; }
        .war-room-header {
            font-family: 'Orbitron', sans-serif;
            color: var(--primary);
            text-align: center;
            padding: 20px;
            border: 2px solid var(--primary);
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
            margin-bottom: 30px;
        }
        .tactical-card {
            background: var(--surface);
            border-left: 4px solid var(--primary);
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        .metric-title { font-size: 0.75rem; color: #888; text-transform: uppercase; }
        .metric-value { font-family: 'Orbitron'; font-size: 1.8rem; color: var(--primary); }
        .stButton>button {
            width: 100%; border-radius: 4px; height: 3.8em;
            background: linear-gradient(90deg, #004d13 0%, #00ff41 100%) !important;
            color: black !important; font-weight: 800; font-family: 'Orbitron'; border: none;
        }
        </style>
    """, unsafe_allow_html=True)
local_css()
# --- 2. FONCTINS ANALYTIQUES ---
def estimate_metrics(reviews, rating, price):
    """Algorithme de prédiction de volume (Ratio FR)"""
    factor = 65 
    monthly_sales = int((reviews / 12) * factor * (1.2 if rating > 4.4 else 0.8))
    monthly_sales = max(5, monthly_sales)
    revenue = monthly_sales * price
    return monthly_sales, revenue
def get_keywords(titles):
    words = []
    stopwords = ["le", "la", "les", "de", "des", "un", "une", "pour", "avec", "a", "et", "en", "sur", "du", "au"]
    for title in titles:
        clean = re.sub(r'[^\w\s]', '', title.lower())
        words.extend([w for w in clean.split() if len(w) > 2 and w not in stopwords])
    return Counter(words).most_common(10)
def get_amazon_suggestions(keyword):
    if not keyword: return []
    try:
        url = f"https://completion.amazon.fr/search/complete?search-alias=aps&client=amazon-search-ui&m=A13V1IB3VIYZZH&q={urllib.parse.quote(keyword)}&lc=fr_FR"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            res = r.json()
            if len(res) > 1: return res[1]
    except: return []
    return []
# --- 3. MOTEUR D'EXTRACTION RÉELLE (SCRAPER BRUT) ---
@st.cache_data(ttl=600)
def fetch_real_amazon_data(query):
    """Scraper brut sans redirection ni simulation."""
    data = []
    url = f"https://www.amazon.fr/s?k={urllib.parse.quote_plus(query)}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if "captcha" in response.text.lower() or response.status_code != 200:
            return None, "🔥 BLOQUÉ PAR AMAZON : L'IP du serveur est repérée. Le scraping réel est impossible pour le moment."
        soup = BeautifulSoup(response.content, "lxml")
        items = soup.find_all("div", {"data-component-type": "s-search-result"})
        
        if not items:
            return None, "📵 AUCUN RÉSULTAT : Amazon n'a retourné aucun produit."
        for i in items[:15]:
            try:
                # 1. Titre
                title_tag = i.h2
                if not title_tag: continue
                t = title_tag.text.strip()
                
                # 2. Prix (Extraction précise)
                p_whole = i.find("span", "a-price-whole")
                p_frac = i.find("span", "a-price-fraction")
                if p_whole:
                    price_str = "".join(filter(str.isdigit, p_whole.text)) or "0"
                    frac_str = "".join(filter(str.isdigit, p_frac.text)) if p_frac else "00"
                    p = float(f"{price_str}.{frac_str}")
                else: continue # On ignore les produits sans prix affiché
                
                # 3. Note
                rt_tag = i.find("span", {"class": "a-icon-alt"})
                rt = 4.0
                if rt_tag:
                    rt_match = re.search(r"(\d[,\.]\d)", rt_tag.text)
                    if rt_match: rt = float(rt_match.group(1).replace(',', '.'))
                
                # 4. Avis
                av_tag = i.find("span", {"class": "a-size-base", "dir": "auto"})
                av = 0
                if av_tag and any(c.isdigit() for c in av_tag.text):
                    av = int("".join(filter(str.isdigit, av_tag.text)))
                # 5. Lien réel vers le vendeur
                link_tag = i.h2.find("a", href=True)
                link = "https://www.amazon.fr" + link_tag['href'].split('/ref=')[0] if link_tag else "#"
                sales, rev = estimate_metrics(av, rt, p)
                data.append({
                    "💎 Produit": t[:70] + "...", 
                    "Prix (€)": p, "Note": rt, "Avis": av, 
                    "Ventes/Mois": sales, "CA/Mois (€)": int(rev),
                    "Lien": link
                })
            except: continue
        if not data:
            return None, "⚠️ ERREUR PARSING : Impossible de lire les prix sur cette page Amazon."
            
        return pd.DataFrame(data), None
    except Exception as e:
        return None, f"🌋 ERREUR TECHNIQUE : {str(e)}"
# --- 4. INTERFACE ---
st.markdown("""
<div class='war-room-header'>
    <h1 style='margin:0; letter-spacing:5px;'>🛡️ SNIPER OS : LIVE DATA FR</h1>
    <p style='margin:0; opacity:0.7;'>DONNÉES RÉELLES AMZ.FR // REVENUS ESTIMÉS</p>
</div>
""", unsafe_allow_html=True)
if 'data' not in st.session_state: st.session_state.data = None
if 'query_input' not in st.session_state: st.session_state.query_input = ""
with st.sidebar:
    st.markdown("### 🛠️ CIBLE")
    query = st.text_input("RECHERCHE PRODUIT", value=st.session_state.query_input, placeholder="ex: fontaine chat inox")
    st.session_state.query_input = query
    
    if st.button("🚀 LANCER LE SCAN RÉEL"):
        if query:
            with st.spinner("Extraction des revenus Amazon France en cours..."):
                df, err = fetch_real_amazon_data(query)
                if err: st.error(err)
                else: st.session_state.data = df
        else: st.warning("Entrez un produit.")
    st.divider()
    st.markdown("### 🔍 AUTO-SUGGESTIONS")
    if query:
        if st.button("DÉCOUVRIR SOUS-NICHES"):
            sugs = get_amazon_suggestions(query)
            if sugs:
                for s in sugs[:8]:
                    if st.button(f"🎯 {s.upper()}", key=f"s_{s}"):
                        st.session_state.query_input = s
                        st.rerun()
# --- DASHBOARD ---
if st.session_state.data is not None:
    df = st.session_state.data
    
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='tactical-card'><div class='metric-title'>Revenu Estimé</div><div class='metric-value'>{int(df['CA/Mois (€)'].sum())}€</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='tactical-card'><div class='metric-title'>Ventes Moy.</div><div class='metric-value'>{int(df['Ventes/Mois'].mean())}</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='tactical-card'><div class='metric-title'>Prix Moyen</div><div class='metric-value'>{round(df['Prix (€)'].mean(), 2)}€</div></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='tactical-card'><div class='metric-title'>Note Moyenne</div><div class='metric-value'>{round(df['Note'].mean(), 1)}/5</div></div>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["📊 X-RAY (REEL)", "🔍 SEO MOTS-CLÉS", "💰 CALCUL PROFIT"])
    
    with t1:
        st.dataframe(
            df, 
            use_container_width=True,
            column_config={"Lien": st.column_config.LinkColumn("Lien Amazon", display_text="Lien Vendeur 🔗")},
            hide_index=True
        )
        st.download_button("📥 Télécharger DATA (CSV)", df.to_csv(index=False), "sniper_data.csv")
    with t2:
        kw = get_keywords(df["💎 Produit"].tolist())
        st.write("### Mots-clés les plus utilisés par les vendeurs :")
        for word, count in kw:
            st.markdown(f"- **{word.upper()}** ({count} fois)")
    with t3:
        p_v = st.number_input("Prix de Vente (€)", value=float(round(df['Prix (€)'].mean(), 2)))
        p_a = st.number_input("Prix d'Achat (DDP) (€)", value=10.0)
        
        comm = p_v * 0.15
        fba = 5.5
        tva = p_v * 0.20
        profit = p_v - p_a - comm - fba - tva
        
        st.metric("Net Profit / Unité", f"{round(profit, 2)} €", delta=f"{int((profit/p_v)*100)}% Marge")
        st.info(f"Profit Mensuel Potentiel : **{int(profit * df['Ventes/Mois'].mean())} €**")
else:
    st.info("🛰️ En attente de cible Amazon France.")
