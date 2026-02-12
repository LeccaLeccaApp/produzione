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

st.title("🍦 Smart Lab Lecca-Lecca")

# --- 1. INSERIMENTO VOCALE / TESTO ---
st.subheader("🎤 Dettatura Ordine (Multiplo)")
input_testo = st.text_area("Esempio: 'Terminato nocciola, fragola 4kg, liquirizia'", height=100)

if st.button("🚀 ELABORA TUTTO L'ORDINE"):
    fasi = input_testo.upper().replace('.', ',').split(',')
    aggiunti = 0
    for frase in fasi:
        for gusto in RICETTE.keys():
            if gusto in frase:
                kg_m = re.search(r'(\d+)', frase)
                kg = float(kg_m.group(1)) if kg_m else 7.0
                st.session_state.produzione.append({"gusto": gusto, "kg": kg, "seq": RICETTE[gusto]['seq']})
                aggiunti += 1
    if aggiunti > 0:
        st.success(f"Caricati {aggiunti} gusti!")
    else:
        st.warning("Nessun gusto riconosciuto.")

# --- 2. FOTOCAMERA (SIDEBAR) ---
with st.sidebar:
    st.header("📸 Fatture")
    foto = st.camera_input("Scatta")
    if foto: st.success("Foto salvata")

# --- 3. GENERAZIONE DOCUMENTO UNICO ---
if st.session_state.produzione:
    st.divider()
    if st.button("🖨️ GENERA FILE PER STAMPA UNICA", use_container_width=True):
        data_s = datetime.now().strftime("%d/%m/%Y")
        lotto_s = datetime.now().strftime("%Y%m%d")
        df_p = pd.DataFrame(st.session_state.produzione).sort_values(by="seq")
        
        # --- BLOCCO 1: CARTA DEL GELATIERE ---
        txt = "--- 1. CARTA DEL GELATIERE ---\n" + "="*30 + "\n"
        u_s = None
        for _, r in df_p.iterrows():
            if u_s is not None and r['seq'] != u_s:
                txt += "\n🚿 RISCIACQUO MACCHINA\n" + "-"*30 + "\n" [cite: 2026-02-11]
            txt += f"\n🍦 {r['gusto']} ({r['kg']} KG)\n"
            for i_n, d_o in RICETTE[r['gusto']]['ing']:
                p_e = int(d_o * (r['kg']/7.0))
                txt += f"  - {i_n}: {p_e}g\n"
            u_s = r['seq']

        # --- BLOCCO 2: ETICHETTE ---
        txt += "\n\n--- 2. ETICHETTE NUTRIZIONALI ---\n" + "="*30 + "\n"
        for _, r in df_p.iterrows():
            txt += f"\n🏷️ {r['gusto']} | Lotto: {lotto_s}\nCalorie: {RICETTE[r['gusto']]['kcal']} kcal/100g\n"
            txt += "."*20 + "\n"

        # --- BLOCCO 3: RIEPILOGO E FIRME ---
        txt += "\n\n--- 3. RIEPILOGO GIORNALIERO ---\n" + "="*30 + "\n"
        txt += f"Data: {data_s} | Lotto: {lotto_s}\n\n"
        for _, r in df_p.iterrows():
            txt += f"[ ] {r['gusto']} - {r['kg']} KG\n"
        txt += "\n\nFirma Franco Antonio: __________________\n"
        txt += "Firma Quagliozzi Giuseppe: ________________\n"

        st.download_button("💾 SCARICA TUTTO PER STAMPA", txt, f"Produzione_{lotto_s}.txt")

    # Anteprima lista
    for p in st.session_state.produzione:
        st.write(f"✅ {p['gusto']} ({p['kg']} KG)")
    
    if st.button("🗑️ Svuota"):
        st.session_state.produzione = []; st.rerun()
