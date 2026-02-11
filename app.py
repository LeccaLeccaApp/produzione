import streamlit as st
import pandas as pd

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

st.title("🍦 Gestione Produzione")

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
    # 1. GENERAZIONE TESTO PER STAMPA UNICA
    report_stampa = "LISTA PRODUZIONE LECCA-LECCA\n" + "="*30 + "\n\n"
    df = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
    ultimo_s = None
    
    for i, row in df.iterrows():
        if ultimo_s is not None and row['seq'] != ultimo_s:
            report_stampa += "\n🚿 RISCIACQUO MACCHINA\n" + "-"*30 + "\n"
        
        report_stampa += f"\n👉 {row['gusto']} ({row['kg']} KG)\n"
        for ing, dose in RICETTE[row['gusto']]['ing']:
            report_stampa += f"- {ing}: {int(dose * (row['kg']/7.0) if row['kg']!=7.0 else dose)}g\n"
        report_stampa += f"Etichetta: {RICETTE[row['gusto']]['kcal']} kcal/100g\n"
        ultimo_s = row['seq']

    # --- TASTO STAMPA GENERALE ---
    st.download_button(
        label="🖨️ STAMPA TUTTA LA LISTA (PDF/TXT)",
        data=report_stampa,
        file_name=f"produzione_{datetime.now().strftime('%d_%m')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.divider()

    # 2. VISUALIZZAZIONE A SCHERMO
    ultimo_s = None
    for i, row in df.iterrows():
        if ultimo_s is not None and row['seq'] != ultimo_s:
            st.error("🚿 RISCIACQUO MACCHINA") [cite: 2026-02-11]
            
        with st.expander(f"📖 {row['gusto']} - {row['kg']} KG", expanded=True):
            for ing, dose in RICETTE[row['gusto']]['ing']:
                st.write(f"- {ing}: **{int(dose * (row['kg']/7.0) if row['kg']!=7.0 else dose)}g**")
        ultimo_s = row['seq']

    if st.button("✅ FINE E PULISCI"):
        st.session_state.produzione = []; st.session_state.attiva = False; st.rerun()
