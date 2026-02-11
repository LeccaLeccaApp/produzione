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
if 'spese' not in st.session_state: st.session_state.spese = []

st.title("🍦 Laboratorio Lecca-Lecca")

# --- MENU LATERALE ---
with st.sidebar:
    st.header("📝 1. Scegli Gusti")
    gusto = st.selectbox("Seleziona", sorted(list(RICETTE.keys())))
    kg = st.number_input("Quantità (KG)", value=7.0, step=0.5)
    if st.button("AGGIUNGI ALLA LISTA"):
        st.session_state.piano_lavoro.append({"gusto": gusto, "kg": kg, "seq": RICETTE[gusto]['seq']})
        st.session_state.in_produzione = False

    if st.session_state.piano_lavoro and not st.session_state.in_produzione:
        st.divider()
        if st.button("🚀 MANDA IN PRODUZIONE", use_container_width=True):
            st.session_state.in_produzione = True

    st.divider()
    st.header("📸 2. Foto Fatture")
    foto = st.camera_input("Scatta")
    if foto:
        with st.form("f"):
            forn = st.text_input("Fornitore")
            imp = st.number_input("€ Totale", step=0.01)
            det = st.text_area("Articoli")
            if st.form_submit_button("SALVA"):
                st.session_state.spese.append({"forn": forn, "tot": imp, "det": det, "data": datetime.now().strftime("%d/%m")})

# --- AREA CENTRALE ---
t1, t2 = st.tabs(["🚀 PRODUZIONE", "📊 CONTABILITÀ & REPORT"])

with t1:
    if st.session_state.in_produzione:
        df = pd.DataFrame(st.session_state.piano_lavoro).sort_values(by="seq")
        last_s = None
        for _, row in df.iterrows():
            # Corretta logica risciacquo senza errori di sintassi
            if last_s is not None and row['seq'] != last_s:
                st.error("RISCIACQUO MACCHINA OBBLIGATORIO")
            
            with st.expander(f"RICETTA: {row['gusto']} - {row['kg']} KG", expanded=True):
                for ing, dose in RICETTE[row['gusto']]['ing']:
                    st.write(f"- {ing}: **{int(dose * row['kg'])}g**")
            last_s = row['seq']
        
        if st.button("✅ FINE LAVORO"):
            st.session_state.piano_lavoro = []
            st.session_state.in_produzione = False
            st.rerun()
    else:
        st.info("Scegli i gusti a sinistra e clicca sul razzo 🚀")

with t2:
    st.subheader("Riepilogo per Email")
    report = "RIEPILOGO FATTURE\n"
    for s in st.session_state.spese:
        st.info(f"{s['forn']} (€{s['tot']})")
        report += f"{s['forn']} - €{s['tot']}\n"
    st.text_area("Copia questo testo per Nicola:", report)
