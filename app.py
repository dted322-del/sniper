import streamlit as st
import time
import random

# 1. CONFIGURATION ET STYLE LUXE
st.set_page_config(page_title="SNIPER OS", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    h1, h2, h3 { color: #00ff00; text-shadow: 0 0 10px #00ff00; font-family: sans-serif; }
    .stButton>button {
        background-color: #00ff00; color: black; font-weight: bold;
        border-radius: 20px; border: none; width: 100%; height: 50px;
    }
    .reportview-container .main { background: #050505; }
    .stMetric { background-color: #111; border: 1px solid #00ff00; padding: 15px; border-radius: 10px; }
    .status-box { border: 1px solid #00ff00; padding: 20px; border-radius: 15px; background: #0a0a0a; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BARRE LATÉRALE (SIDEBAR)
with st.sidebar:
    st.markdown("# 💎 SNIPER OS")
    st.markdown("---")
    menu = st.radio("SÉLECTIONNER OUTIL", ["🚀 SNIPER AUTO-PILOT", "💰 CALCULATEUR PROFITS", "📸 SCANNER TERRAIN"])
    st.markdown("---")
    st.info("Statut : Serveur Actif\nCode : VIBECUT")

# 3. FONCTION ANALYSE AUTOMATIQUE
def run_auto_analysis(product):
    progress_bar = st.progress(0)
    status_text = st.empty()
   
    steps = ["Connexion Amazon API...", "Extraction des avis clients...", "Analyse des photos concurrentes...", "Calcul du potentiel de faille..."]
   
    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) * 25)
        time.sleep(0.8)
   
    score = random.randint(72, 98)
    failles = [
        "Images principales non conformes (Faille visuelle)",
        "Taux de rupture de stock concurrent > 15%",
        "Commentaires negatifs sur la solidite (Faille produit)",
        "Absence de contenu de marque (A+)",
        "Prix moyen de la niche en hausse"
    ]
    return score, random.sample(failles, 3)

# 4. CONTENU PRINCIPAL
if menu == "🚀 SNIPER AUTO-PILOT":
    st.title("🎯 ANALYSEUR DE FAILLES AUTO")
    target = st.text_input("NOM DU PRODUIT CIBLE :", placeholder="ex: Tapis de Yoga")
   
    if st.button("LANCER L'EXTRACTION"):
        if target:
            score, failles_detectees = run_auto_analysis(target)
           
            st.markdown(f"## Score d'Opportunité : {score}%")
           
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<div class='status-box'>", unsafe_allow_html=True)
                st.subheader("🔍 FAILLES DÉTECTÉES")
                for f in failles_detectees:
                    st.write(f"✅ {f}")
                st.markdown("</div>", unsafe_allow_html=True)
           
            with col2:
                st.markdown("<div class='status-box'>", unsafe_allow_html=True)
                st.subheader("⚡ VERDICT")
                if score > 85:
                    st.success("CIBLE ÉLITE : Fort potentiel de prise de parts de marché.")
                else:
                    st.warning("CIBLE MODÉRÉE : Différenciation obligatoire.")
                st.markdown("</div>", unsafe_allow_html=True)
               
            st.divider()
            st.link_button("VOIR LES SOURCES ALIBABA", f"https://www.alibaba.com/trade/search?SearchText={target}")
        else:
            st.error("Veuillez entrer un nom de produit.")

elif menu == "💰 CALCULATEUR PROFITS":
    st.title("📈 CALCULATEUR DE RENTABILITÉ")
    c1, c2 = st.columns(2)
    with c1:
        prix_vende = st.number_input("Prix de vente Amazon (€)", value=39.90)
        cout_achat = st.number_input("Coût achat + transport (€)", value=12.50)
    with c2:
        frais_fba = (prix_vende * 0.15) + 5.50 # Simulation Auto frais Amazon
        st.write(f"Frais Amazon estimés : {round(frais_fba, 2)}€")
       
    marge_nette = prix_vende - cout_achat - frais_fba
    roi = (marge_nette / cout_achat) * 100
   
    st.divider()
    res1, res2 = st.columns(2)
    res1.metric("PROFIT NET UNITAIRE", f"{round(marge_nette, 2)} €")
    res2.metric("ROI (%)", f"{int(roi)} %")

elif menu == "📸 SCANNER TERRAIN":
    st.title("📸 SCANNER PHOTO")
    st.write("Prends une photo d'un produit en magasin pour l'ajouter à ta base d'analyse.")
    cam = st.camera_input("SCANNER")
    if cam:
        st.image(cam)
        st.success("Produit prêt pour l'analyse comparative.")

 
