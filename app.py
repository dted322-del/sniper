mport streamlit as st

# Setup de base
st.set_page_config(page_title="SNIPER OS", page_icon="🎯")

st.markdown("# 🎯 SNIPER OS : OPERATIONNEL")
st.success("L'application fonctionne enfin !")

# Menu simple
menu = st.sidebar.radio("MENU", ["Recherche", "Calculateur"])

if menu == "Recherche":
    niche = st.text_input("Produit a analyser :", "Yoga")
    st.write(f"Analyse pour : {niche}")
    st.link_button("VOIR SUR AMAZON", f"https://www.amazon.fr/s?k={niche}")

if menu == "Calculateur":
    ca = st.number_input("Chiffre d'affaires mensuel vise (EUR) :", value=1000)
    profit = ca * 0.25
    st.metric("Profit Net Estime (25%)", f"{profit} EUR")

 
