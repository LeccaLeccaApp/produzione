import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Lecca-Lecca ERP & Contabilità", layout="wide")

# --- DATABASE RICETTE ---
RICETTE = {
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 130)], "seq": 1},
    "OREO": {"ing": [("Base Bianca", 900), ("Pasta Cookies Black", 50)], "seq": 2},
    "GALAK": {"ing": [("Base Bianca", 825), ("Panna Suldy", 150), ("Pasta Galak", 100)], "seq": 2},
    "LIMONE": {"ing": [("Acqua", 700), ("Lemon Plus", 300)], "seq": 3},
    "FONDENTE": {"ing": [("Acqua", 600), ("Fondente", 450)], "seq": 12},
}

# Inizializzazione memorie
if 'produzione' not in st.session_state: st.session_state.produzione = []
if 'spese' not in st.session_state: st.session_state.spese = []

st.title("🍦 Sistema Integrato Lecca-Lecca")

# --- BARRA LATERALE ---
with st.sidebar:
    st.header("📸 Carica Fattura/Scontrino")
    foto = st.camera_input("Scatta")
    if foto:
        st.success("Immagine acquisita!")
        with st.form("dati_fattura"):
            fornitore = st.text_input("Fornitore (es. Saima)")
            data_f = st.date_input("Data Fattura", datetime.now())
            importo = st.number_input("Importo Totale (€)", step=0.01)
            dettaglio = st.text_area("Articoli (es: Latte 20lt 24€, Panna 10lt 40€)")
            if st.form_submit_button("SALVA IN CONTABILITÀ"):
                st.session_state.spese.append({
                    "mese": data_f.strftime("%m/%Y"),
                    "fornitore": fornitore,
                    "data": data_f.strftime("%d/%m/%y"),
                    "totale": importo,
                    "dettaglio": dettaglio
                })
                st.balloons()

# --- PANNELLO CENTRALE ---
tab1, tab2, tab3 = st.tabs(["🚀 PRODUZIONE", "📊 CONTABILITÀ MESE", "📧 INVIO PDF"])

with tab1:
    st.subheader("Pianifica Lavoro")
    c1, c2 = st.columns(2)
    with c1: g = st.selectbox("Gusto", list(RICETTE.keys()))
    with c2: k = st.number_input("KG", value=7.0)
    if st.button("AGGIUNGI"):
        st.session_state.produzione.append({"gusto": g, "kg": k, "seq": RICETTE[g]['seq']})
    
    # Lista con Risciacquo [2026-02-11]
    df = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
    last_s = None
    for _, row in df.iterrows():
        if last_s is not None and row['seq'] != last_s:
            st.error("🚿 RISCIACQUO")
        st.write(f"**{row['gusto']}** - {row['kg']}kg")
        last_s = row['seq']

with tab2:
    st.subheader(f"Riepilogo {datetime.now().strftime('%B %Y')}")
    if st.session_state.spese:
        for s in st.session_state.spese:
            st.info(f"**{s['fornitore']}** - Fattura del {s['data']}: **€{s['totale']}**")
            st.write(f"Dettaglio: {s['dettaglio']}")
    else:
        st.write("Nessuna spesa registrata questo mese.")

with tab3:
    st.write("L'invio del PDF a **cristianonicola84@gmail.com** avverrà l'ultimo giorno del mese.")
    if st.button("GENERA ANTEPRIMA PDF"):
        st.warning("Funzione di generazione PDF in fase di attivazione su server...")
