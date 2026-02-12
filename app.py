import streamlit as st
import pandas as pd
from datetime import datetime
import re

st.set_page_config(page_title="Lecca-Lecca Smart Lab", layout="wide")

# --- DATABASE RICETTE ---
RICETTE = {
    "NOCCIOLA VEGANO": {"ing": [("Acqua", 4375), ("Pasta Nocciola", 910), ("Zuccheri", 2450)], "seq": 1, "kcal": 210},
    "BUENO VEGANO": {"ing": [("Acqua", 625), ("Pasta Bueno Veg", 120)], "seq": 1, "kcal": 225},
    "STRACCIATELLA": {"ing": [("Base Lecca lecca", 7000), ("Cioccolato scaglie", 560)], "seq": 2, "kcal": 240},
    "GALAK": {"ing": [("Base Bianca", 825), ("Pasta Galak", 100)], "seq": 2, "kcal": 260},
    "FRAGOLA": {"ing": [("Acqua", 2100), ("Polpa Fragola", 2625), ("Base", 1400)], "seq": 3, "kcal": 150},
    "LIMONE": {"ing": [("Acqua", 700), ("Succo Limone", 300)], "seq": 3, "kcal": 130},
    "LIQUIRIZIA": {"ing": [("Acqua", 5000), ("Liquirizia", 500)], "seq": 4, "kcal": 180},
    "FONDENTE": {"ing": [("Acqua", 600), ("Fondente 70%", 450)], "seq": 12, "kcal": 280}
}

if 'produzione' not in st.session_state: st.session_state.produzione = []
if 'spese' not in st.session_state: st.session_state.spese = []

st.title("🍦 Smart Laboratorio Lecca-Lecca")

# --- 1. INSERIMENTO RAPIDO (VOCALE/TESTO) ---
st.subheader("🎤 Inserimento Rapido")
input_testo = st.text_area("Esempio: 'Terminato nocciola', 'Liquirizia mancano 2kg'", placeholder="Scrivi o usa il microfono...")

if st.button("ELABORA ORDINE"):
    # Logica per estrarre gusto e kg dal testo
    testo = input_testo.upper()
    gusto_trovato = None
    for g in RICETTE.keys():
        if g in testo:
            gusto_trovato = g
            break
    
    if gusto_trovato:
        # Cerca i KG nel testo, altrimenti usa default 7
        kg_match = re.search(r'(\d+)\s*KG', testo)
        kg = float(kg_match.group(1)) if kg_match else 7.0
        st.session_state.produzione.append({"gusto": gusto_trovato, "kg": kg, "seq": RICETTE[gusto_trovato]['seq']})
        st.success(f"Aggiunto: {gusto_trovato} ({kg} KG)")
    else:
        st.error("Gusto non riconosciuto. Riprova.")

# --- 2. FOTOCAMERA FATTURE ---
with st.sidebar:
    st.header("📸 Fatture & Spese")
    foto = st.camera_input("Scatta")
    if foto:
        with st.form("f_spesa"):
            forn = st.text_input("Fornitore")
            imp = st.number_input("€", step=0.01)
            if st.form_submit_button("SALVA"):
                st.session_state.spese.append({"f": forn, "e": imp, "d": datetime.now().strftime("%d/%m")})

# --- 3. TASTO ORDINA ADESSO (GENERA DOCUMENTO UNICO) ---
if st.session_state.produzione:
    st.divider()
    if st.button("🚀 ORDINA ADESSO (GENERA TUTTO)", use_container_width=True):
        data_o = datetime.now().strftime("%d/%m/%Y")
        lotto = datetime.now().strftime("%Y%m%d")
        
        # --- COSTRUZIONE FILE UNICO ---
        doc = f"--- RIEPILOGO GIORNALIERO PRODUZIONE ({data_o}) ---\n"
        doc += f"Lotto: {lotto}\n"
        doc += "Firme: Franco Antonio / Quagliozzi Giuseppe\n"
        doc += "="*40 + "\n\n"
        
        df = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
        u_s = None
        
        sezione_etichette = "\n" + "="*40 + "\n--- SEZIONE ETICHETTE ---\n"
        sezione_gelatiere = "\n" + "="*40 + "\n--- CARTA DEL GELATIERE ---\n"
        
        for _, row in df.iterrows():
            # Risciacquo macchina [cite: 2026-02-11]
            if u_s is not None and row['seq'] != u_s:
                sezione_gelatiere += "\n🚿 RISCIACQUO MACCHINA\n"
            
            # Parte Gelatiere (Dosi)
            sezione_gelatiere += f"\n👉 {row['gusto']} ({row['kg']} KG)\n"
            for ing, dose in RICETTE[row['gusto']]['ing']:
                p = int(dose * (row['kg']/7.0))
                sezione_gelatiere += f"  - {ing}: {p}g\n"
            
            # Parte Etichette
            sezione_etichette += f"\n🏷️ {row['gusto']}\nValore energetico: {RICETTE[row['gusto']]['kcal']} kcal/100g\n"
            
            u_s = row['seq']
        
        final_file = doc + sezione_gelatiere + sezione_etichette
        
        st.download_button(
            label="🖨️ SCARICA E STAMPA DOCUMENTO UNICO",
            data=final_file,
            file_name=f"Produzione_{lotto}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Visualizzazione veloce a schermo
    for p in st.session_state.produzione:
        st.write(f"✅ In lista: {p['gusto']} - {p['kg']} KG")
    
    if st.button("🗑️ Svuota Lista"):
        st.session_state.produzione = []; st.rerun()
