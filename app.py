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
# 1. CONFIGURATION &amp; DESIGN SYSTÈME LUXE
# ==========================================
st.set_page_config(page_title=&quot;SNIPER OS PRESTIGE&quot;, page_icon=&quot;��&quot;,
layout=&quot;wide&quot;)

st.markdown(&quot;&quot;&quot;
&lt;style&gt;
@import
url(&#39;https://fonts.googleapis.com/css2?family=Orbitron:wght@700&amp;family=Inter:wght
@300;400;700;900&amp;display=swap&#39;);

:root { --neon: #00ff00; --bg: #030303; }
html, body, [class*=&quot;st-&quot;] { font-family: &#39;Inter&#39;, sans-serif; background-color: var(--
bg); color: white; }

.glow-title {
font-family: &#39;Orbitron&#39;, sans-serif; color: var(--neon);
text-shadow: 0 0 20px rgba(0,255,0,0.4); text-align: center; margin-bottom:
2rem;

}

.elite-card {
background: rgba(255, 255, 255, 0.03);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 20px;
overflow: hidden;
transition: 0.4s ease;
margin-bottom: 20px;
}
.elite-card:hover { border-color: var(--neon); transform: translateY(-5px); box-
shadow: 0 10px 30px rgba(0, 255, 0, 0.1); }

.product-img { width: 100%; height: 250px; object-fit: cover; border-bottom: 1px
solid rgba(255, 255, 255, 0.08); }
.card-content { padding: 20px; }
.badge { background: var(--neon); color: black; padding: 4px 12px; border-radius:
20px; font-size: 0.7rem; font-weight: bold; font-family: &#39;Orbitron&#39;; }

.stButton&gt;button {
background: linear-gradient(135deg, #00ff00 0%, #008800 100%);
color: black !important; border: none; border-radius: 12px; font-weight: 800;
height: 3.5rem; text-transform: uppercase; width: 100%;
}
&lt;/style&gt;
&quot;&quot;&quot;, unsafe_allow_stdio=True)

# ==========================================
# 2. LOGIQUE MÉTIER (IMAGES &amp; PDF)
# ==========================================

@st.cache_data
def get_product_img(category, index):
return
f&quot;https://source.unsplash.com/featured/800x600?{category},product,luxury&amp;sig={inde
x}&quot;

def calculate_projection(ca_mensuel, marge_percent):
mois = [&quot;Mois 1&quot;, &quot;Mois 2&quot;, &quot;Mois 3&quot;, &quot;Mois 4&quot;, &quot;Mois 5&quot;, &quot;Mois 6&quot;]
croissance = [1, 1.4, 2.1, 3.0, 4.2, 5.8]
profits = [int((ca_mensuel * (marge_percent/100)) * c * 0.85) for c in croissance]
return pd.DataFrame({&quot;Mois&quot;: mois, &quot;Profit Net (€)&quot;: profits})

def generate_pdf_report(df, total_net, product_name):
pdf = FPDF()
pdf.add_page()
pdf.set_fill_color(10, 10, 10)
pdf.rect(0, 0, 210, 297, &#39;F&#39;)
pdf.set_text_color(0, 255, 0)
pdf.set_font(&quot;Arial&quot;, &#39;B&#39;, 24)
pdf.cell(190, 40, &quot;RAPPORT SNIPER OS ELITE&quot;, ln=True, align=&#39;C&#39;)
pdf.set_text_color(255, 255, 255)
pdf.set_font(&quot;Arial&quot;, &#39;B&#39;, 14)
pdf.cell(190, 10, f&quot;PRODUIT : {product_name.upper()}&quot;, ln=True, align=&#39;C&#39;)
pdf.ln(20)
pdf.set_font(&quot;Arial&quot;, &#39;&#39;, 12)
pdf.cell(100, 10, f&quot;Date d&#39;analyse : {datetime.date.today()}&quot;, ln=True)
pdf.cell(100, 10, f&quot;Profit Cumule (6 mois) : {total_net} EUR&quot;, ln=True)
pdf.ln(10)
for index, row in df.iterrows():
pdf.cell(100, 10, f&quot;{row[&#39;Mois&#39;]} : {row[&#39;Profit Net (€)&#39;]} EUR&quot;, ln=True)

return pdf.output(dest=&#39;S&#39;).encode(&#39;latin-1&#39;)

# ==========================================
# 3. INTERFACE (SIDEBAR &amp; SCANNER)
# ==========================================
with st.sidebar:
st.markdown(&quot;&lt;h1 style=&#39;color:#00ff00; font-family:Orbitron;&#39;&gt;SNIPER OS&lt;/h1&gt;&quot;,
unsafe_allow_stdio=True)
st.divider()
source = st.radio(&quot;SOURCE PHOTO :&quot;, [&quot;Scanner Direct&quot;, &quot;Importer Image&quot;])
user_img = None
if source == &quot;Scanner Direct&quot;:
cam_shot = st.camera_input(&quot;Scan&quot;)
if cam_shot: user_img = Image.open(cam_shot)
else:
file_up = st.file_uploader(&quot;Fichier&quot;, type=[&#39;jpg&#39;, &#39;png&#39;])
if file_up: user_img = Image.open(file_up)

if user_img:
st.image(user_img, caption=&quot;Cible Identifiée&quot;, use_column_width=True)
decoded = decode(user_img)
if decoded: st.success(f&quot;EAN : {decoded[0].data.decode(&#39;utf-8&#39;)}&quot;)
st.divider()
st.info(&quot;Code UGC : VIBECUT&quot;)

# ==========================================
# 4. DASHBOARD CENTRAL (ONGLETS)
# ==========================================
st.markdown(&quot;&lt;h1 class=&#39;glow-title&#39;&gt;DOMINATION AMAZON FBA&lt;/h1&gt;&quot;,
unsafe_allow_stdio=True)

tabs = st.tabs([&quot;�� RADAR&quot;, &quot;��️ VALIDATEUR&quot;, &quot;�� LOGISTIQUE&quot;, &quot;�� BUSINESS
PLAN&quot;])

# --- TAB 1 : RADAR ---
with tabs[0]:
query = st.text_input(&quot;QUELLE NICHE ANALYSER ?&quot;, placeholder=&quot;Ex: Yoga,
Cuisine, Fitness...&quot;)
if query:
cols = st.columns(2)
for i in range(2):
with cols[i]:
niche = f&quot;{query} {[&#39;PREMIUM&#39;, &#39;COMPACT&#39;][i]}&quot;
img_url = get_product_img(query, i)
st.markdown(f&quot;&quot;&quot;&lt;div class=&quot;elite-card&quot;&gt;
&lt;img src=&quot;{img_url}&quot; class=&quot;product-img&quot;&gt;
&lt;div class=&quot;card-content&quot;&gt;
&lt;span class=&quot;badge&quot;&gt;POTENTIEL 100%&lt;/span&gt;
&lt;h3 style=&quot;margin:10px 0;&quot;&gt;{niche}&lt;/h3&gt;
&lt;p style=&quot;color:#888; font-size:0.8rem;&quot;&gt;Packaging noir mat et logo
premium recommandes.&lt;/p&gt;
&lt;/div&gt;
&lt;/div&gt;&quot;&quot;&quot;, unsafe_allow_stdio=True)
st.link_button(&quot;�� ANALYSER LA FAILLE&quot;,
f&quot;https://www.amazon.fr/s?k={urllib.parse.quote(niche)}&quot;)

# --- TAB 2 : VALIDATEUR ---
with tabs[1]:
st.subheader(&quot;��️ Algorithme Anti-Echec&quot;)
c1, c2 = st.columns(2)
with c1:

v1 = st.toggle(&quot;Poids &lt; 1.2kg (Frais FBA bas)&quot;)
v2 = st.toggle(&quot;Prix de Vente &gt; 35€ (Marge saine)&quot;)
with c2:
v3 = st.toggle(&quot;Avis concurrents &lt; 4.2★ (Opportunite)&quot;)
v4 = st.toggle(&quot;Pas d&#39;electronique (SAV faible)&quot;)
score = sum([v1, v2, v3, v4])
if score == 4: st.success(&quot;�� SIGNAL D&#39;ACHAT : 100% - PRODUIT GAGNANT&quot;)
else: st.metric(&quot;SCORE DE VIABILITÉ&quot;, f&quot;{int((score/4)*100)}%&quot;)

# --- TAB 3 : LOGISTIQUE DDP ---
with tabs[2]:
st.subheader(&quot;�� Coût de Revient Réel&quot;)
cl1, cl2 = st.columns(2)
with cl1:
pu = st.number_input(&quot;Prix Achat Usine ($)&quot;, value=10.0)
fr = st.number_input(&quot;Transport DDP ($)&quot;, value=3.0)
with cl2:
pv = st.number_input(&quot;Prix Vente Amazon (€)&quot;, value=49.90)
f_amz = (pv * 0.15) + 7.50
revient = (pu + fr) * 0.94 * 1.05
profit = pv - revient - f_amz
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric(&quot;Prix Livré&quot;, f&quot;{round(revient, 2)}€&quot;)
m2.metric(&quot;Profit Net&quot;, f&quot;{round(profit, 2)}€&quot;)
m3.metric(&quot;Marge %&quot;, f&quot;{round((profit/pv)*100, 1)}%&quot;)

# --- TAB 4 : PROJECTION &amp; PDF ---
with tabs[3]:

st.subheader(&quot;�� Projection Financière (6 mois)&quot;)
ca_init = st.number_input(&quot;CA Mensuel de départ (€)&quot;, value=10000)
marge_s = st.slider(&quot;Marge Nette souhaitée (%)&quot;, 10, 50, 25)
df = calculate_projection(ca_init, marge_s)

fig = px.area(df, x=&quot;Mois&quot;, y=&quot;Profit Net (€)&quot;, color_discrete_sequence=[&#39;#00ff00&#39;])
fig.update_layout(paper_bgcolor=&#39;rgba(0,0,0,0)&#39;, plot_bgcolor=&#39;rgba(0,0,0,0)&#39;,
font_color=&quot;white&quot;)
st.plotly_chart(fig, use_container_width=True)

total_net = df[&quot;Profit Net (€)&quot;].sum()
st.markdown(f&quot;&lt;div style=&#39;border:1px solid #00ff00; padding:20px; text-
align:center; border-radius:15px;&#39;&gt;&lt;h3&gt;CUMUL NET PRÉVU : {total_net}
€&lt;/h3&gt;&lt;/div&gt;&quot;, unsafe_allow_stdio=True)

st.divider()
pdf_bytes = generate_pdf_report(df, total_net, query if query else &quot;Produit
Inconnu&quot;)
st.download_button(label=&quot;�� TÉLÉCHARGER LE RAPPORT PDF ÉLITE&quot;,
data=pdf_bytes, file_name=&quot;Rapport_Sniper_OS.pdf&quot;, mime=&quot;application/pdf&quot;)
