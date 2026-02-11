import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Lecca-Lecca", layout="wide")

# Database essenziale
RICETTE = {
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 130)], "seq": 1},
    "BUENO VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 50)], "seq": 1},
    "OREO": {"ing": [("Base Bianca", 900), ("Pasta Cookies", 50)], "seq": 2},
    "STRACCIATELLA": {"ing": [("Base Latte", 1000), ("Cioccolato", 80)], "seq": 2},
    "FRAGOLA": {"ing": [("Acqua", 300), ("Polpa", 375), ("Base", 200)], "seq": 3},
    "FONDENTE": {"ing": [("Acqua", 600), ("Fondente", 450)], "seq": 4},
}

if 'lista' not in st.session_state: st.session_state.lista = []
if 'vai' not in st.session_state: st.session_state.vai = False

st.sidebar.header("📝 Inserimento")
g = st.sidebar.selectbox("Gusto", sorted(RICETTE.keys()))
k = st.sidebar.number_input("KG", 7.0)
if st.sidebar.button("AGGIUNGI"):
    st.session_state.lista.append({"g": g, "k": k, "s": RICETTE[g]['seq']})
    st.session_state.vai = False

if st.session_state.lista and not st.session_state.vai:
    if st.sidebar.button("🚀 MANDA IN PRODUZIONE"):
        st.session_state.vai = True

st.title("🍦 Produzione Lecca-Lecca")

if st.session_state.vai:
    ls = None
    for r in sorted(st.session_state.lista, key=lambda x: x['s']):
        if ls is not None and r['s'] != ls:
            st.error("🚿 RISCIACQUO MACCHINA") # [cite: 2026-02-11]
        with st.expander(f"{r['g']} - {r['k']} KG", expanded=True):
            for i, d in RICETTE[r['g']]['ing']:
                st.write(f"- {i}: {int(d * r['k'])}g")
        ls = r['s']
    if st.button("✅ FINE"):
        st.session_state.lista = []; st.session_state.vai = False; st.rerun()
else:
    st.info("Aggiungi i gusti a sinistra e clicca il Razzo 🚀")
