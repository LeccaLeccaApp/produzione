import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Lecca-Lecca Produzione", layout="wide")

# Database Ricette
RICETTE = {
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 130), ("DX", 37.5)], "seq": 1},
    "BUENO VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 50)], "seq": 1},
    "OREO": {"ing": [("Base Bianca", 900), ("Pasta Cookies Black", 50)], "seq": 2},
    "STRACCIATELLA": {"ing": [("Base Lecca lecca", 1000), ("Cioccolato scaglie", 80)], "seq": 2},
    "FRAGOLA": {"ing": [("Acqua", 300), ("Polpa Fragola", 375), ("Base", 200)], "seq": 3},
    "FONDENTE": {"ing": [("Acqua", 600), ("Fondente", 450)], "seq": 12},
}

if 'piano_lavoro' not in st.session_state: st.session_state.piano_lavoro = []
if 'in_produzione' not in st.session_state: st.session_state.in_produzione = False

st.title("🍦 Laboratorio Lecca-Lecca")

# --- BARRA LATERALE ---
with st.sidebar:
    st.header("📝 Pianifica")
    gusto = st.selectbox("Seleziona", sorted(list(RICETTE.keys())))
    kg = st.number_input("KG", value=7.0, step=0.5)
    
    if st.button("AGGIUNGI AL PIANO"):
        st.session_state.piano_lavoro.append({"gusto": gusto, "kg": kg, "seq": RICETTE[gusto]['seq']})
        st.session_state.in_produzione = False

    st.divider()
    if st.session_state.piano_lavoro:
        st.write("Lista d'attesa:")
        for p in st.session_state.piano_lavoro:
            st.text(f"• {p['gusto']} ({p['kg']}kg)")
        
        # IL TASTO CHE VOLEVI
        if st.button("🚀 MANDA IN PRODUZIONE", use_container_width=True):
            st.session_state.in_produzione = True

# --- AREA DI LAVORO ---
if st.session_state.in_produzione:
    st.header("👨‍🍳 PRODUZIONE ATTIVA")
    df = pd.DataFrame(st.session_state.piano_lavoro).sort_values(by="seq")
    last_s = None
    
    for _, row in df.iterrows():
        # Logica risciacquo 
        if last_s is not None and row['seq'] != last_s:
            st.error("🚿 RISCIACQUO MACCHINA") 
        
        with st.expander(f"📖 {row['gusto']} - {row['kg']} KG", expanded=True):
            for ing, dose in RICETTE[row['gusto']]['ing']:
                st.write(f"- {ing}: **{int(dose * row['kg'])}g**")
        last_s = row['seq']
    
    if st.button("✅ FINE LAVORO"):
        st.session_state.piano_lavoro = []
        st.session_state.in_produzione = False
        st.rerun()
else:
    st.info("Scegli i gusti a sinistra e poi clicca sul tasto razzo 🚀")
