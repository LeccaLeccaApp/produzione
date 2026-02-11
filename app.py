import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Lecca-Lecca ERP", layout="wide")

# Database Ricette - Pulito e senza errori
RICETTE = {
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 130), ("DX", 37.5)], "seq": 1},
    "BUENO VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 50)], "seq": 1},
    "OREO": {"ing": [("Base Bianca", 900), ("Pasta Cookies Black", 50)], "seq": 2},
    "STRACCIATELLA": {"ing": [("Base Lecca lecca", 1000), ("Cioccolato scaglie", 80)], "seq": 2},
    "FRAGOLA": {"ing": [("Acqua", 300), ("Polpa Fragola", 375), ("Base", 200)], "seq": 3},
    "FONDENTE": {"ing": [("Acqua", 600), ("Fondente", 450)], "seq": 4},
}

if 'piano' not in st.session_state: st.session_state.piano = []
if 'attiva' not in st.session_state: st.session_state.attiva = False
if 'spese' not in st.session_state: st.session_state.spese = []

st.title("🍦 Laboratorio Lecca-Lecca")

# --- MENU LATERALE ---
with st.sidebar:
    st.header("📝 1. Scegli Gusti")
    g = st.selectbox("Gusto", sorted(list(RICETTE.keys())))
    k = st.number_input("KG", value=7.0, step=0.5)
    if st.button("AGGIUNGI ALLA LISTA"):
        st.session_state.piano.append({"gusto": g, "kg": k, "seq": RICETTE[g]['seq']})
        st.session_state.attiva = False

    if st.session_state.piano and not st.session_state.attiva:
        st.divider()
        st.write("Gusti pronti:")
        for p in st.session_state.piano:
            st.text(f"- {p['gusto']}")
        
        # TASTO PER MANDARE IN PRODUZIONE
        if st.button("🚀 MANDA IN PRODUZIONE", use_container_width=True):
            st.session_state.attiva = True

    st.divider()
    st.header("📸 2. Fatture")
    foto = st.camera_input("Scatta")
    if foto:
        with st.form("f"):
            forn = st.text_input("Fornitore")
            imp = st.number_input("€", step=0.01)
            if st.form_submit_button("SALVA"):
                st.session_state.spese.append({"f": forn, "t": imp, "d": datetime.now().strftime("%d/%m")})

# --- AREA DI LAVORO ---
t1, t2 = st.tabs(["🚀 PRODUZIONE", "📊 CONTABILITÀ"])

with t1:
    if st.session_state.attiva:
        df = pd.DataFrame(st.session_state.piano).sort_values(by="seq")
        ls = None
        for _, row in df.iterrows():
            if ls is not None and row['seq'] != ls:
                st.error("🚿 RISCIACQUO MACCHINA") # [cite: 2026-02-11]
            with st.expander(f"📖 {row['gusto']} - {row['kg']} KG", expanded=True):
                for ing, dose in RICETTE[row['gusto']]['ing']:
                    st.write(f"- {ing}: **{int(dose * row['kg'])}g**")
            ls = row['seq']
        
        if st.button("✅ FINE LAVORO"):
            st.session_state.piano = []
            st.session_state.attiva = False
            st.rerun()
    else:
        st.info("Aggiungi i gusti a sinistra e clicca il razzo 🚀")

with t2:
    st.subheader("Riepilogo")
    for s in st.session_state.spese:
        st.info(f"{s['f']} - €{s['t']}")
