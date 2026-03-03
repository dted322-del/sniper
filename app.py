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

# 1. STYLE LUXE
st.set_page_config(page_title=&quot;SNIPER OS PRESTIGE&quot;, page_icon=&quot;��&quot;,
layout=&quot;wide&quot;)

st.markdown(&quot;&quot;&quot;
&lt;style&gt;
.stApp { background-color: #030303; color: white; }
.glow { color: #00ff00; text-align: center; font-family: sans-serif; }
&lt;/style&gt;
&quot;&quot;&quot;, unsafe_allow_stdio=True)

# 2. LOGIQUE
@st.cache_data
def get_img(cat, i):
return f&quot;https://source.unsplash.com/featured/800x600?{cat},product&amp;sig={i}&quot;

# 3. INTERFACE
st.markdown(&quot;&lt;h1 class=&#39;glow&#39;&gt;SNIPER OS ELITE&lt;/h1&gt;&quot;, unsafe_allow_stdio=True)

with st.sidebar:
st.title(&quot;Scanner&quot;)
st.camera_input(&quot;Prendre une photo&quot;)
st.info(&quot;Code : VIBECUT&quot;)

tabs = st.tabs([&quot;�� RADAR&quot;, &quot;�� PROFIT&quot;])

with tabs[0]:
query = st.text_input(&quot;Niche :&quot;, &quot;Fitness&quot;)
if query:
st.image(get_img(query, 1), width=300)
st.link_button(&quot;Rechercher sur Amazon&quot;, f&quot;https://www.amazon.fr/s?k={query}&quot;)

with tabs[1]:
ca = st.number_input(&quot;CA mensuel vise (€)&quot;, value=10000)
marge = st.slider(&quot;Marge %&quot;, 10, 50, 25)
st.metric(&quot;Profit Net&quot;, f&quot;{int(ca * marge / 100)} €&quot;)
