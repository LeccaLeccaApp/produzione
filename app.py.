import streamlit as st
import pandas as pd

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Lecca-Lecca ERP", layout="wide")

# --- DATABASE RICETTE (Aggiornato dalle tue foto) ---
RICETTE = {
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 130), ("DX", 37.5)], "seq": 1},
    "BUENO VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 50)], "seq": 1},
    "OREO": {"ing": [("Base Bianca", 900), ("Pasta Cookies Black", 50)], "seq": 2},
    "RED VELVET": {"ing": [("Base Bianca", 900), ("Pasta Cookies Black", 50)], "seq": 2},
    "GALAK": {"ing": [("Base Bianca", 825), ("Panna Suldy", 150), ("Pasta Cioccolato Bianco", 100)], "seq": 2},
    "FIOR DI LATTE": {"ing": [("Base Lecca lecca", 1000)], "seq": 2},
    "STRACCIATELLA": {"ing": [("Base Lecca lecca", 1000), ("Cioccolato scaglie", 80)], "seq": 2},
    "LIMONE": {"ing": [("Acqua", 700), ("Lemon Plus", 300)], "seq": 3},
    "FRAGOLA": {"ing": [("Acqua", 300), ("Polpa Fragola", 375), ("Base", 200), ("DX", 40), ("SX", 75)], "seq": 3},
    "MANGO": {"ing": [("Acqua", 700), ("Mango", 300)], "seq": 4},
    "CARAMELLO SALATO": {"ing": [("Latte Intero", 750), ("Caramello Salato", 312.5)], "seq": 5},
    "ZUPPA INGLESE": {"ing": [("Base Bianca", 900), ("Panna Suldy", 100), ("Pasta Zuppa Inglese", 30)], "seq": 7},
    "FONDENTE": {"ing": [("Acqua", 600), ("Fondente", 450), ("DX", 20)], "seq": 12},
}

# --- LOGICA APPLICAZIONE ---
if 'ordini' not in st.session_state:
    st.session_state.ordini = []

st.title("🍦 Produzione Gelateria Lecca-Lecca")
st.write("Via Aldo Moro, 61")

# Interfaccia Sidebar per iPhone
with st.sidebar:
    st.header("Aggiungi Gusto")
    scelta = st.selectbox("Seleziona Gusto", sorted(list(RICETTE.keys())))
    kg = st.number_input("Quantità (KG)", min_value=0.5, value=7.0, step=0.5)
    if st.button("AGGIUNGI ALL'ORDINE"):
        st.session_state.ordini.append({"gusto": scelta, "kg": kg, "seq": RICETTE[scelta]['seq']})

# Visualizzazione Risultati
if st.session_state.ordini:
    # Ordiniamo per la sequenza corretta (1-14)
    df_ordini = pd.DataFrame(st.session_state.ordini).sort_values(by="seq")
    
    st.subheader("📋 Lista Produzione Ordinata")
    
    last_seq = None
    for _, row in df_ordini.iterrows():
        # LOGICA RISCIACQUO: Se la sequenza cambia, inseriamo l'avviso
        if last_seq is not None and row['seq'] != last_seq:
            st.error("🚿 RISCIACQUO MACCHINA OBBLIGATORIO")
        
        # Scheda del gusto
        with st.expander(f"✅ {row['gusto']} - {row['kg']} KG", expanded=True):
            ricetta = RICETTE[row['gusto']]
            for ingrediente, dose_base in ricetta['ing']:
                totale = dose_base * row['kg']
                st.write(f"- {ingrediente}: **{int(totale)}g**")
        
        last_seq = row['seq']

    if st.button("🗑️ SVUOTA TUTTA LA LISTA"):
        st.session_state.ordini = []
        st.rerun()
else:
    st.info("La lista è vuota. Aggiungi i gusti dal menu a sinistra.")
