import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Lecca-Lecca Lab", layout="wide")

# Database Ricette
RICETTE = {
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 4375), ("Pasta Nocciola", 910), ("Zuccheri", 2450)], "seq": 1, "kcal": 210},
    "BUENO VEGANO": {"ing": [("Acqua", 625), ("Pasta Bueno Veg", 120)], "seq": 1, "kcal": 225},
    "STRACCIATELLA": {"ing": [("Base Lecca lecca", 7000), ("Cioccolato scaglie", 560)], "seq": 2, "kcal": 240},
    "GALAK": {"ing": [("Base Bianca", 825), ("Pasta Galak", 100)], "seq": 2, "kcal": 260},
    "FRAGOLA": {"ing": [("Acqua", 2100), ("Polpa Fragola", 2625), ("Base", 1400)], "seq": 3, "kcal": 150},
    "LIMONE": {"ing": [("Acqua", 700), ("Succo Limone", 300)], "seq": 3, "kcal": 130},
    "FONDENTE": {"ing": [("Acqua", 600), ("Fondente 70%", 450)], "seq": 12, "kcal": 280}
}

if 'produzione' not in st.session_state: st.session_state.produzione = []
if 'attiva' not in st.session_state: st.session_state.attiva = False

st.title("🍦 Gestione Produzione Unica")

with st.sidebar:
    st.header("🛒 Selezione")
    g_scelto = st.selectbox("Gusto", list(RICETTE.keys()))
    kg = st.number_input("KG", value=7.0, step=0.5)
    if st.button("AGGIUNGI"):
        st.session_state.produzione.append({"gusto": g_scelto, "kg": kg, "seq": RICETTE[g_scelto]['seq']})
        st.session_state.attiva = False

    if st.session_state.produzione and not st.session_state.attiva:
        if st.button("🚀 AVVIA PRODUZIONE", use_container_width=True):
            st.session_state.attiva = True

if st.session_state.attiva:
    # --- COSTRUZIONE UNICA DEL REPORT PER STAMPA ---
    data_oggi = datetime.now().strftime('%d/%m/%Y')
    testo_finale = f"📋 REPORT PRODUZIONE - {data_oggi}\n"
    testo_finale += "="*40 + "\n\n"
    
    df = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
    ultimo_s = None
    
    for _, row in df.iterrows():
        # Logica risciacquo automatica tra sequenze diverse [cite: 2026-02-11]
        if ultimo_s is not None and row['seq'] != ultimo_s:
            testo_finale += "\n🚿 RISCIACQUO MACCHINA OBBLIGATORIO\n"
            testo_finale += "-"*40 + "\n"
        
        testo_finale += f"\n🍦 GUSTO: {row['gusto']} ({row['kg']} KG)\n"
        for ing, dose in RICETTE[row['gusto']]['ing']:
            # Calcolo proporzionale se i KG sono diversi da 7
            peso = int(dose * (row['kg']/7.0)) if row['kg'] != 7.0 else int(dose)
            testo_finale += f"  - {ing}: {peso}g\n"
        
        testo_finale += f"🏷️ Etichetta: {RICETTE[row['gusto']]['kcal']} kcal/100g\n"
        testo_finale += "."*40 + "\n"
        ultimo_s = row['seq']

    # --- TASTO STAMPA UNICO ---
    st.subheader("🖨️ Documento pronto per la stampa")
    st.download_button(
        label="CLICCA QUI PER STAMPARE TUTTA LA LISTA",
        data=testo_finale,
        file_name=f"Produzione_{datetime.now().strftime('%d_%m')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.divider()
    
    # Visualizzazione rapida a schermo (facoltativa)
    st.text(testo_finale)

    if st.button("✅ FINE E SVUOTA"):
        st.session_state.produzione = []; st.session_state.attiva = False; st.rerun()
