import streamlit as st
import pandas as pd
import urllib.parse
import random
import datetime
from PIL import Image
from pyzbar.pyzbar import decode
import plotly.express as px
from fpdf import FPDF
import io

# ==========================================
# 1. CONFIGURATION & DESIGN SYSTÈME LUXE
# ==========================================
st.set_page_config(page_title="SNIPER OS PRESTIGE", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@300;400;700;900&display=swap');
   
    :root { --neon: #00ff00; --bg: #030303; }
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: var(--bg); color: white; }
   
    .glow-title {
        font-family: 'Orbitron', sans-serif; color: var(--neon);
        text-shadow: 0 0 20px rgba(0,255,0,0.4); text-align: center; margin-bottom: 2rem;
    }

    .elite-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        overflow: hidden;
        transition: 0.4s ease;
        margin-bottom: 20px;
    }
    .elite-card:hover { border-color: var(--neon); transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0, 255, 0, 0.1); }
   
    .product-img { width: 100%; height: 250px; object-fit: cover; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
    .card-content { padding: 20px; }
    .badge { background: var(--neon); color: black; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: bold; font-family: 'Orbitron'; }

    .stButton>button {
        background: linear-gradient(135deg, #00ff00 0%, #008800 100%);
        color: black !important; border: none; border-radius: 12px; font-weight: 800; height: 3.5rem; text-transform: uppercase; width: 100%;
    }
    </style>
    """, unsafe_allow_stdio=True)

# ==========================================
# 2. LOGIQUE MÉTIER (IMAGES & PDF)
# ==========================================
@st.cache_data
def get_product_img(category, index):
    return f"https://source.unsplash.com/featured/800x600?{category},product,luxury&sig={index}"

def calculate_projection(ca_mensuel, marge_percent):
    mois = ["Mois 1", "Mois 2", "Mois 3", "Mois 4", "Mois 5", "Mois 6"]
    croissance = [1, 1.4, 2.1, 3.0, 4.2, 5.8]
    profits = [int((ca_mensuel * (marge_percent/100)) * c * 0.85) for c in croissance]
    return pd.DataFrame({"Mois": mois, "Profit Net (€)": profits})

def generate_pdf_report(df, total_net, product_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(10, 10, 10)
    pdf.rect(0, 0, 210, 297, 'F')
    pdf.set_text_color(0, 255, 0)
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(190, 40, "RAPPORT SNIPER OS ELITE", ln=True, align='C')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(190, 10, f"PRODUIT : {product_name.upper()}", ln=True, align='C')
    pdf.ln(20)
    pdf.set_font("Arial", '', 12)
    pdf.cell(100, 10, f"Date d'analyse : {datetime.date.today()}", ln=True)
    pdf.cell(100, 10, f"Profit Cumule (6 mois) : {total_net} EUR", ln=True)
    pdf.ln(10)
    for index, row in df.iterrows():
        pdf.cell(100, 10, f"{row['Mois']} : {row['Profit Net (€)']} EUR", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 3. INTERFACE (SIDEBAR & SCANNER)
# ==========================================
with st.sidebar:
    st.markdown("<h1 style='color:#00ff00; font-family:Orbitron;'>SNIPER OS</h1>", unsafe_allow_stdio=True)
    st.divider()
    source = st.radio("SOURCE PHOTO :", ["Scanner Direct", "Importer Image"])
    user_img = None
    if source == "Scanner Direct":
        cam_shot = st.camera_input("Scan")
        if cam_shot: user_img = Image.open(cam_shot)
    else:
        file_up = st.file_uploader("Fichier", type=['jpg', 'png'])
        if file_up: user_img = Image.open(file_up)
   
    if user_img:
        st.image(user_img, caption="Cible Identifiée", use_column_width=True)
        decoded = decode(user_img)
        if decoded: st.success(f"EAN : {decoded[0].data.decode('utf-8')}")
    st.divider()
    st.info("Code UGC : VIBECUT")

# ==========================================
# 4. DASHBOARD CENTRAL (ONGLETS)
# ==========================================
st.markdown("<h1 class='glow-title'>DOMINATION AMAZON FBA</h1>", unsafe_allow_stdio=True)
tabs = st.tabs(["🚀 RADAR", "🛡️ VALIDATEUR", "🚢 LOGISTIQUE", "📈 BUSINESS PLAN"])

# --- TAB 1 : RADAR ---
with tabs[0]:
    query = st.text_input("QUELLE NICHE ANALYSER ?", placeholder="Ex: Yoga, Cuisine, Fitness...")
    if query:
        cols = st.columns(2)
        for i in range(2):
            with cols[i]:
                niche = f"{query} {['PREMIUM', 'COMPACT'][i]}"
                img_url = get_product_img(query, i)
                st.markdown(f"""<div class="elite-card">
                    <img src="{img_url}" class="product-img">
                    <div class="card-content">
                        <span class="badge">POTENTIEL 100%</span>
                        <h3 style="margin:10px 0;">{niche}</h3>
                        <p style="color:#888; font-size:0.8rem;">Packaging noir mat et logo premium recommandes.</p>
                    </div>
                </div>""", unsafe_allow_stdio=True)
                st.link_button("💥 ANALYSER LA FAILLE", f"https://www.amazon.fr/s?k={urllib.parse.quote(niche)}")

# --- TAB 2 : VALIDATEUR ---
with tabs[1]:
    st.subheader("🛡️ Algorithme Anti-Echec")
    c1, c2 = st.columns(2)
    with c1:
        v1 = st.toggle("Poids < 1.2kg (Frais FBA bas)")
        v2 = st.toggle("Prix de Vente > 35€ (Marge saine)")
    with c2:
        v3 = st.toggle("Avis concurrents < 4.2★ (Opportunite)")
        v4 = st.toggle("Pas d'electronique (SAV faible)")
    score = sum([v1, v2, v3, v4])
    if score == 4: st.success("🎯 SIGNAL D'ACHAT : 100% - PRODUIT GAGNANT")
    else: st.metric("SCORE DE VIABILITÉ", f"{int((score/4)*100)}%")

# --- TAB 3 : LOGISTIQUE DDP ---
with tabs[2]:
    st.subheader("🚢 Coût de Revient Réel")
    cl1, cl2 = st.columns(2)
    with cl1:
        pu = st.number_input("Prix Achat Usine ($)", value=10.0)
        fr = st.number_input("Transport DDP ($)", value=3.0)
    with cl2:
        pv = st.number_input("Prix Vente Amazon (€)", value=49.90)
        f_amz = (pv * 0.15) + 7.50
    revient = (pu + fr) * 0.94 * 1.05
    profit = pv - revient - f_amz
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Prix Livré", f"{round(revient, 2)}€")
    m2.metric("Profit Net", f"{round(profit, 2)}€")
    m3.metric("Marge %", f"{round((profit/pv)*100, 1)}%")

# --- TAB 4 : PROJECTION & PDF ---
with tabs[3]:
    st.subheader("📈 Projection Financière (6 mois)")
    ca_init = st.number_input("CA Mensuel de départ (€)", value=10000)
    marge_s = st.slider("Marge Nette souhaitée (%)", 10, 50, 25)
    df = calculate_projection(ca_init, marge_s)
   
    fig = px.area(df, x="Mois", y="Profit Net (€)", color_discrete_sequence=['#00ff00'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)
   
    total_net = df["Profit Net (€)"].sum()
    st.markdown(f"<div style='border:1px solid #00ff00; padding:20px; text-align:center; border-radius:15px;'><h3>CUMUL NET PRÉVU : {total_net} €</h3></div>", unsafe_allow_stdio=True)
   
    st.divider()
    pdf_bytes = generate_pdf_report(df, total_net, query if query else "Produit Inconnu")
    st.download_button(label="📥 TÉLÉCHARGER LE RAPPORT PDF ÉLITE", data=pdf_bytes, file_name="Rapport_Sniper_OS.pdf", mime="application/pdf")

 
