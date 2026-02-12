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
}

if 'produzione' not in st.session_state: st.session_state.produzione = []
if 'spese' not in st.session_state: st.session_state.spese = []

st.title("🍦 Smart Lab: Carta, Etichette e Riepilogo")

# --- 1. INSERIMENTO VOCALE / TESTO ---
st.subheader("🎤 Dettatura Ordine")
input_testo = st.text_area("Dì tutto quello che serve (es: 'Terminato nocciola, mancano 3kg fragola')", height=150)

if st.button("🚀 ELABORA TUTTO L'ORDINE", use_container_width=True):
    linee = input_testo.upper().split(',') # Divide per virgola o punto se dettato
    trovati = 0
    for frase in linee:
        for gusto in RICETTE.keys():
            if gusto in frase:
                kg_match = re.search(r'(\d+)', frase)
                kg = float(kg_match.group(1)) if kg_match else 7.0
                st.session_state.produzione.append({"gusto": gusto, "kg": kg, "seq": RICETTE[gusto]['seq']})
                trovati += 1
    if trovati > 0:
        st.success(f"Ho aggiunto {trovati} gusti alla lista!")
    else:
        st.error("Non ho riconosciuto gusti. Prova a scandire bene il nome.")

# --- 2. FOTO FATTURE (SIDEBAR) ---
with st.sidebar:
    st.header("📸 Fatture")
    foto = st.camera_input("Scatta")
    if foto:
        st.success("Fattura acquisita!")

# --- 3. GENERAZIONE DOCUMENTO UNICO ---
if st.session_state.produzione:
    st.divider()
    if st.button("🖨️ GENERA FILE PER STAMPA UNICA", use_container_width=True):
        data_o = datetime.now().strftime("%d/%m/%Y")
        lotto = datetime.now().strftime("%Y%m%d")
        df = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
        
        # --- PARTE 1: CARTA DEL GELATIERE ---
        corpo_gelatiere = f"1. CARTA DEL GELATIERE - {data_o}\n" + "="*40 + "\n"
        u_s = None
        for _, row in df.iterrows():
            if u_s is not None and row['seq'] != u_s:
                corpo_gelatiere += "\n🚿 RISCIACQUO MACCHINA OBBLIGATORIO\n" [cite: 2026-02-11]
                corpo_gelatiere += "-"*40 + "\n"
            corpo_gelatiere += f"\n🍦 {row['gusto']} ({row['kg']} KG)\n"
            for ing, dose in RICETTE[row['gusto']]['ing']:
                p = int(dose * (row['kg']/7.0))
                corpo_gelatiere += f"  - {ing}: {p}g\n"
            u_s = row['seq']

        # --- PARTE 2: ETICHETTE ---
        corpo_etichette = "\n\n2. ETICHETTE NUTRIZIONALI\n" + "="*40 + "\n"
        for _, row in df.iterrows():
            corpo_etichette += f"\n🏷️ PRODOTTO: {row['gusto']}\nLotto: {lotto}\nCalorie: {RICETTE[row['gusto']]['kcal']} kcal/100g\n"
            corpo_etichette += "."*20 + "\n"

        # --- PARTE 3: RIEPILOGO E FIRME ---
        corpo_riepilogo = "\n\n3. RIEPILOGO GIORNALIERO\n" + "="*40 + "\n"
        corpo_riepilogo += f"Data: {data_o} | Lotto Unico: {lotto}\n\n"
        for _, row in df.iterrows():
            corpo_riepilogo += f"[ ] {row['gusto']} - {row['kg']} KG\n"
        corpo_riepilogo += "\n\nFirma Responsabile 1: Franco Antonio ________________\n"
        corpo_riepilogo += "Firma Responsabile 2: Quagliozzi Giuseppe ______________\n"

        file_finale = corpo_gelatiere + corpo_etichette + corpo_riepilogo
        
        st.download_button(
            label="💾 SCARICA DOCUMENTO COMPLETO",
            data=file_finale,
            file_name=f"Produzione_Completa_{lotto}.txt",
            mime="text/plain",
            use_container_width=True
        )

    # Elenco visivo
    st.write("### 📋 Gusti pronti per l'ordine:")
    for i, p in enumerate(st.session_state.produzione):
        st.write(f"{i+1}. {p['gusto']} - {p['kg']} KG")
    
    if st.button("🗑️ Svuota Tutto"):
        st.session_state.produzione = []; st.rerun()
