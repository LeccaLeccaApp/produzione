import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lecca-Lecca ERP", layout="wide")

# Database Ricette
RICETTE = {
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 130), ("DX", 37.5)], "seq": 1},
    "OREO": {"ing": [("Base Bianca", 900), ("Pasta Cookies Black", 50)], "seq": 2},
    "GALAK": {"ing": [("Base Bianca", 825), ("Panna Suldy", 150), ("Pasta Cioccolato Bianco", 100)], "seq": 2},
    "LIMONE": {"ing": [("Acqua", 700), ("Lemon Plus", 300)], "seq": 3},
    "FONDENTE": {"ing": [("Acqua", 600), ("Fondente", 450), ("DX", 20)], "seq": 12},
}

if 'produzione' not in st.session_state:
    st.session_state.produzione = []

st.title("🍦 Gestione Lecca-Lecca")

# --- BARRA LATERALE ---
with st.sidebar:
    st.header("➕ Nuovo Inserimento")
    tipo_lista = st.radio("Quando devi produrre?", ["Oggi", "Domani"])
    gusto = st.selectbox("Gusto", sorted(list(RICETTE.keys())))
    kg = st.number_input("Quantità (KG)", value=7.0, step=0.5)
    
    if st.button("AGGIUNGI IN LISTA"):
        st.session_state.produzione.append({"gusto": gusto, "kg": kg, "quando": tipo_lista, "seq": RICETTE[gusto]['seq']})
    
    st.divider()
    st.header("📸 Gestione Fatture")
    foto = st.camera_input("Scatta foto fattura")
    if foto:
        st.success("Fattura acquisita correttamente!")

# --- PANNELLO CENTRALE ---
tab1, tab2 = st.tabs(["🚀 PRODUZIONE OGGI", "📅 PIANO PER DOMANI"])

def mostra_lista(periodo):
    lista = [item for item in st.session_state.produzione if item['quando'] == periodo]
    if lista:
        df = pd.DataFrame(lista).sort_values(by="seq")
        last_s = None
        for _, row in df.iterrows():
            if last_s is not None and row['seq'] != last_s:
                st.error("🚿 RISCIACQUO") # Rispetto la sequenza Nicola! [2026-02-11]
            
            with st.expander(f"{row['gusto']} - {row['kg']} KG"):
                for ing, dose in RICETTE[row['gusto']]['ing']:
                    st.write(f"- {ing}: {int(dose * row['kg'])}g")
            last_s = row['seq']
    else:
        st.info(f"Nessuna produzione prevista per {periodo.lower()}.")

with tab1:
    mostra_lista("Oggi")

with tab2:
    mostra_lista("Domani")

if st.button("🗑️ SVUOTA TUTTO"):
    st.session_state.produzione = []
    st.rerun()
