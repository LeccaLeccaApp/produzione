import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Lecca-Lecca ERP Globale", layout="wide")

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

st.title("🍦 Gestione Integrale Lecca-Lecca")

# --- BARRA LATERALE ---
with st.sidebar:
    st.header("📝 Pianifica Produzione")
    gusto = st.selectbox("Seleziona Gusto", sorted(list(RICETTE.keys())))
    kg = st.number_input("Quantità (KG)", value=7.0, step=0.5)
    if st.button("AGGIUNGI AL PIANO"):
        st.session_state.piano_lavoro.append({"gusto": gusto, "kg": kg, "seq": RICETTE[gusto]['seq']})
        st.session_state.in_produzione = False
    
    if st.session_state.piano_lavoro:
        if st.button("🚀 MANDA IN PRODUZIONE", use_container_width=True):
            st.session_state.in_produzione = True

    st.divider()
    st.header("📸 Gestione Fatture")
    foto = st.camera_input("Scatta Foto Fattura") # Torna la fotocamera!
    if foto:
        with st.form("dati_fattura"):
            forn = st.text_input("Fornitore (es. Saima)")
            imp = st.number_input("Importo Totale (€)", step=0.01)
            det = st.text_area("Cosa hai comprato?")
            if st.form_submit_button("CONFERMA E SALVA"):
                st.session_state.spese.append({
                    "forn": forn, 
                    "tot": imp, 
                    "det": det, 
                    "data": datetime.now().strftime("%d/%m/%y")
                })
                st.success("Salvato in contabilità!")

# --- AREA CENTRALE ---
t1, t2 = st.tabs(["🚀 PRODUZIONE", "📊 CONTABILITÀ & MAIL"])

with t1:
    if st.session_state.in_produzione:
        df = pd.DataFrame(st.session_state.piano_lavoro).sort_values(by="seq")
        last_s = None
        for _, row in df.iterrows():
            # Logica risciacquo automatica [cite: 2026-02-11]
            if last_s is not None and row['seq'] != last_s:
                st.error("🚿 RISCIACQUO MACCHINA OBBLIGATORIO")
            with st.expander(f"📖 {row['gusto']} - {row['kg']} KG", expanded=True):
                for ing, dose in RICETTE[row['gusto']]['ing']:
                    st.write(f"- {ing}: **{int(dose * row['kg'])}g**")
            last_s = row['seq']
        
        if st.button("✅ FINE LAVORO (Svuota tutto)"):
            st.session_state.piano_lavoro = []
            st.session_state.in_produzione = False
            st.rerun()
    else:
        st.info("Pianifica i gusti a sinistra e clicca sul tasto 🚀")

with t2:
    st.subheader("Riepilogo per PDF/Mail")
    testo_mail = "RIEPILOGO FATTURE - GESTIONE LECCA-LECCA\n\n"
    for s in st.session_state.spese:
        st.info(f"**{s['forn']}** ({s['data']}): €{s['tot']}")
        testo_mail += f"{s['forn']} del {s['data']} - €{s['tot']}\nNote: {s['det']}\n"
        testo_mail += "-"*20 + "\n"
    
    st.divider()
    st.write("Copia il testo qui sotto e invialo a: **cristianonicola84@gmail.com**")
    st.text_area("Testo pronto per la mail:", testo_mail, height=300)
