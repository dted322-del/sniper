import streamlit as st

# Configuration simple
st.set_page_config(page_title="SNIPER OS", page_icon="🎯")

# Titre principal
st.markdown("# 🎯 SNIPER OS : OPERATIONNEL")
st.success("Bravo ! Connexion reussie.")

# Navigation
page = st.sidebar.selectbox("MENU", ["Radar", "Calculateur"])

if page == "Radar":
    st.header("🚀 Radar de Recherche")
    produit = st.text_input("Produit a analyser :", "Accessoires Fitness")
    st.write(f"Analyse en cours pour : {produit}")
    st.link_button("VOIR SUR AMAZON", f"https://www.amazon.fr/s?k={produit}")

if page == "Calculateur":
    st.header("📈 Calculateur de Profit")
    ca = st.number_input("Chiffre d'affaires mensuel vise (EUR) :", value=1000)
    profit = ca * 0.25
    st.metric("Profit Net estime (25%)", f"{profit} EUR")
 
