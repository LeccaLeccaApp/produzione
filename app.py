import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Lecca-Lecca ERP Completo", layout="wide")

# --- DATABASE INTEGRALE (Tutte le tue ricette) ---
RICETTE = {
    # SEQ 1: VEGANI
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 130), ("DX", 37.5)], "seq": 1},
    "BUENO VEGANO": {"ing": [("Acqua", 625), ("Bianco Stevia", 312), ("Pasta Nocciola", 50)], "seq": 1},
    
    # SEQ 2: CREME LATTE
    "OREO": {"ing": [("Base Bianca", 900), ("Pasta Cookies Black", 50)], "seq": 2},
    "RED VELVET": {"ing": [("Base Bianca", 900), ("Pasta Cookies Black", 50)], "seq": 2},
    "GALAK": {"ing": [("Base Bianca", 825), ("Panna Suldy", 150), ("Pasta Cioccolato Bianco", 100)], "seq": 2},
    "FIOR DI LATTE": {"ing": [("Base Lecca lecca", 1000)], "seq": 2},
    "STRACCIATELLA": {"ing": [("Base Lecca lecca", 1000), ("Cioccolato scaglie", 80)], "seq": 2},
    
    # SEQ 3-4: FRUTTA
    "LIMONE": {"ing": [("Acqua", 700), ("Lemon Plus", 300)], "seq": 3},
    "FRAGOLA": {"ing": [("Acqua", 300), ("Polpa Fragola", 375), ("Base", 200), ("DX", 40), ("SX", 75)], "seq": 3},
    "MANGO": {"ing": [("Acqua", 700), ("Mango", 300)], "seq": 4},
    
    # ALTRE CATEGORIE
    "CARAMELLO SALATO": {"ing": [("Latte Intero", 750), ("Caramello Salato", 312.5)], "seq": 5},
    "ZUPPA INGLESE": {"ing": [("Base Bianca", 900), ("Panna Suldy", 100), ("Pasta Zuppa Inglese", 30)], "seq": 7},
    "FONDENTE": {"ing": [("Acqua", 600), ("Fondente", 450), ("DX", 20)], "seq": 12},
    
    # TORTE E TRONCHETTI (Esempi base da personalizzare)
    "TORTA SEMIFREDDO": {"ing": [("Base Panna", 1000)], "seq": 13},
    "TRONCHETTO": {"ing": [("Base Semifreddo", 1000)], "seq": 13},
}

if 'produzione' not in st.session_state: st.session_state.produzione = []
if 'spese' not in st.session_state: st.session_state.spese = []

st.title("🍦 Gestione Totale Lecca-Lecca")

with st.sidebar:
    st.header("➕ Aggiungi")
    tipo = st.radio("Destinazione", ["Oggi", "Domani"])
    gusto = st.selectbox("Seleziona Prodotto", sorted(list(RICETTE.keys())))
    kg = st.number_input("Quantità (KG)", value=7.0, step=0.5)
    
    if st.button("INSERISCI IN LISTA"):
        st.session_state.produzione.append({"gusto": gusto, "kg": kg, "quando": tipo, "seq": RICETTE[gusto]['seq']})
    
    st.divider()
    st.header("📸 Foto Fatture")
    foto = st.camera_input("Scatta")
    if foto:
        with st.form("dati"):
            forn = st.text_input("Fornitore (es. Saima)")
            imp = st.number_input("Totale €", step=0.01)
            det = st.text_area("Articoli (Latte, Panna, ecc.)")
            if st.form_submit_button("SALVA PER PDF"):
                st.session_state.spese.append({"mese": datetime.now().strftime("%m/%Y"), "forn": forn, "tot": imp, "det": det})
                st.success("Salvato!")

tab1, tab2, tab3 = st.tabs(["🚀 PRODUZIONE", "📊 CONTABILITÀ", "🧪 TABELLE NUTRIZIONALI"])

def mostra(periodo):
    lista = [i for i in st.session_state.produzione if i['quando'] == periodo]
    if lista:
        df = pd.DataFrame(lista).sort_values(by="seq")
        last_s = None
        for _, row in df.iterrows():
            if last_s is not None and row['seq'] != last_s:
                st.error("🚿 RISCIACQUO MACCHINA")
            with st.expander(f"✅ {row['gusto']} - {row['kg']} KG"):
                for ing, dose in RICETTE[row['gusto']]['ing']:
                    st.write(f"- {ing}: **{int(dose * row['kg'])}g**")
            last_s = row['seq']

with tab1:
    st.subheader("Lista di Oggi")
    mostra("Oggi")
    st.divider()
    st.subheader("Lista di Domani")
    mostra("Domani")

with tab2:
    st.write(f"Spese di {datetime.now().strftime('%B %Y')}")
    for s in st.session_state.spese:
        st.info(f"{s['forn']}: €{s['tot']} (Articoli: {s['det']})")

with tab3:
    st.info("Qui appariranno i valori nutrizionali per etichettatura.")
