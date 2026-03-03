import streamlit as st

# Configuration simple sans symboles speciaux
st.set_page_config(page_title=&quot;SNIPER OS&quot;, page_icon=&quot;��&quot;)

st.markdown(&quot;&lt;h1 style=&#39;color:green;&#39;&gt;SNIPER OS CONNECTE&lt;/h1&gt;&quot;,
unsafe_allow_stdio=True)

st.write(&quot;Si tu vois ce message, ton application fonctionne enfin !&quot;)

# Menu de base
choix = st.sidebar.radio(&quot;Menu&quot;, [&quot;Radar&quot;, &quot;Profit&quot;])

if choix == &quot;Radar&quot;:
niche = st.text_input(&quot;Niche a analyser&quot;, &quot;Yoga&quot;)
st.write(f&quot;Analyse en cours pour : {niche}&quot;)
st.link_button(&quot;Chercher sur Amazon&quot;, f&quot;https://www.amazon.fr/s?k={niche}&quot;)

if choix == &quot;Profit&quot;:
ca = st.number_input(&quot;CA mensuel&quot;, value=10000)
st.write(f&quot;Estimation de profit : {int(ca * 0.25)} euros&quot;)
